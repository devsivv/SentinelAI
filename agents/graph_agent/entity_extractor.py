"""
entity_extractor.py — Extract and normalize entities and relationships from input payloads.

Provides normalization functions for different entity types (phone numbers, emails, accounts, UPI IDs)
and extracts entities/relationships from raw multi-modal evidence or pre-extracted records.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple
from .logging import get_logger
from .schemas import Entity, EntityType, Relationship, RelationshipType

log = get_logger()


def normalize_phone(phone: str) -> str:
    """Normalize phone numbers to a digits-only string, preserving '+' prefix if present."""
    if not phone:
        return ""
    cleaned = re.sub(r"[^\d+]", "", phone.strip())
    # Standardize Indian phone number if needed (e.g., removing leading 0 or adding +91)
    if cleaned.startswith("0") and len(cleaned) == 11:
        cleaned = "+91" + cleaned[1:]
    elif len(cleaned) == 10 and not cleaned.startswith("+"):
        cleaned = "+91" + cleaned
    return cleaned


def normalize_email(email: str) -> str:
    """Normalize emails to lowercase and strip whitespaces."""
    if not email:
        return ""
    return email.strip().lower()


def normalize_bank_account(account: str) -> str:
    """Normalize bank account numbers (alphanumeric, uppercase, no spaces)."""
    if not account:
        return ""
    return re.sub(r"\s+", "", account.strip().upper())


def normalize_upi(upi: str) -> str:
    """Normalize UPI IDs to lowercase, removing trailing/leading spaces."""
    if not upi:
        return ""
    return upi.strip().lower()


def normalize_device(device_id: str) -> str:
    """Normalize device IDs to uppercase, stripping spaces."""
    if not device_id:
        return ""
    return device_id.strip().upper()


def normalize_ip(ip: str) -> str:
    """Normalize IP addresses."""
    if not ip:
        return ""
    return ip.strip()


def normalize_url(url: str) -> str:
    """Normalize URLs: lowercase, strip protocol prefixes and query parameters."""
    if not url:
        return ""
    cleaned = url.strip().lower()
    # Remove protocol prefix
    cleaned = re.sub(r"^https?://(www\.)?", "", cleaned)
    # Remove query string
    cleaned = cleaned.split("?")[0]
    # Remove trailing slash
    if cleaned.endswith("/"):
        cleaned = cleaned[:-1]
    return cleaned


def normalize_entity_id(entity_type: EntityType, value: str) -> str:
    """Normalize entity value based on its type."""
    if entity_type == EntityType.PHONE:
        return normalize_phone(value)
    elif entity_type == EntityType.EMAIL:
        return normalize_email(value)
    elif entity_type == EntityType.BANK_ACCOUNT:
        return normalize_bank_account(value)
    elif entity_type == EntityType.UPI:
        return normalize_upi(value)
    elif entity_type == EntityType.DEVICE:
        return normalize_device(value)
    elif entity_type == EntityType.IP:
        return normalize_ip(value)
    elif entity_type == EntityType.URL:
        return normalize_url(value)
    return value.strip()


def extract_and_normalize(
    entities: List[Entity],
    relationships: List[Relationship],
    raw_evidence: List[Dict[str, Any]] | None,
    case_id: str,
) -> Tuple[List[Entity], List[Relationship]]:
    """Normalize input entities/relationships and extract new ones from raw evidence if present."""
    normalized_entities: Dict[Tuple[EntityType, str], Entity] = {}
    normalized_relationships: List[Relationship] = []

    # 1. Add Case node
    case_key = (EntityType.CASE, case_id)
    normalized_entities[case_key] = Entity(
        type=EntityType.CASE,
        id=case_id,
        properties={"created_at": datetime.now(timezone.utc).isoformat()}
    )

    # 2. Normalize and insert explicit entities
    for entity in entities:
        norm_val = normalize_entity_id(entity.type, entity.id)
        if not norm_val:
            continue
        key = (entity.type, norm_val)
        if key in normalized_entities:
            # Merge properties
            normalized_entities[key].properties.update(entity.properties)
        else:
            normalized_entities[key] = Entity(
                type=entity.type,
                id=norm_val,
                properties=entity.properties
            )

    # 3. Normalize and insert explicit relationships
    for rel in relationships:
        src_norm = normalize_entity_id(rel.source_type, rel.source_id)
        tgt_norm = normalize_entity_id(rel.target_type, rel.target_id)
        if not src_norm or not tgt_norm:
            continue
        normalized_relationships.append(
            Relationship(
                source_type=rel.source_type,
                source_id=src_norm,
                target_type=rel.target_type,
                target_id=tgt_norm,
                type=rel.type,
                properties=rel.properties
            )
        )

        # Ensure source and target entity nodes exist in normalized list
        src_key = (rel.source_type, src_norm)
        if src_key not in normalized_entities:
            normalized_entities[src_key] = Entity(type=rel.source_type, id=src_norm)
        tgt_key = (rel.target_type, tgt_norm)
        if tgt_key not in normalized_entities:
            normalized_entities[tgt_key] = Entity(type=rel.target_type, id=tgt_norm)

    # 4. Extract from raw evidence
    if raw_evidence:
        for idx, item in enumerate(raw_evidence):
            input_type = item.get("input_type", "")
            payload = item.get("payload", {})
            if not payload:
                continue

            if input_type == "sms":
                text = payload.get("text", "")
                phone_sender = payload.get("phone", "")
                
                # Extract links/urls and phone numbers from SMS text
                urls = re.findall(r"https?://\S+|www\.\S+", text)
                phones = re.findall(r"\+?\d[\d\s-]{8,14}\d", text)
                
                # Normalize sender phone
                if phone_sender:
                    norm_sender = normalize_phone(phone_sender)
                    sender_key = (EntityType.PHONE, norm_sender)
                    normalized_entities[sender_key] = Entity(type=EntityType.PHONE, id=norm_sender)
                    
                    # Relate Case -> INVOLVES -> Phone
                    normalized_relationships.append(
                        Relationship(
                            source_type=EntityType.CASE,
                            source_id=case_id,
                            target_type=EntityType.PHONE,
                            target_id=norm_sender,
                            type=RelationshipType.INVOLVES
                        )
                    )
                
                for raw_url in urls:
                    norm_url = normalize_url(raw_url)
                    url_key = (EntityType.URL, norm_url)
                    normalized_entities[url_key] = Entity(type=EntityType.URL, id=norm_url)
                    
                    # Case -> SHARES_URL -> URL
                    normalized_relationships.append(
                        Relationship(
                            source_type=EntityType.CASE,
                            source_id=case_id,
                            target_type=EntityType.URL,
                            target_id=norm_url,
                            type=RelationshipType.SHARES_URL
                        )
                    )

                for raw_phone in phones:
                    norm_ph = normalize_phone(raw_phone)
                    if len(norm_ph) >= 10:  # Simple sanity check
                        phone_key = (EntityType.PHONE, norm_ph)
                        normalized_entities[phone_key] = Entity(type=EntityType.PHONE, id=norm_ph)
                        
                        # Case -> SHARES_PHONE -> Phone
                        normalized_relationships.append(
                            Relationship(
                                source_type=EntityType.CASE,
                                source_id=case_id,
                                target_type=EntityType.PHONE,
                                target_id=norm_ph,
                                type=RelationshipType.SHARES_PHONE
                            )
                        )

            elif input_type == "url":
                raw_url = payload.get("url", "")
                if raw_url:
                    norm_url = normalize_url(raw_url)
                    url_key = (EntityType.URL, norm_url)
                    normalized_entities[url_key] = Entity(type=EntityType.URL, id=norm_url)
                    
                    normalized_relationships.append(
                        Relationship(
                            source_type=EntityType.CASE,
                            source_id=case_id,
                            target_type=EntityType.URL,
                            target_id=norm_url,
                            type=RelationshipType.SHARES_URL
                        )
                    )

            elif input_type == "transaction":
                tx_id = f"tx_{case_id}_{idx}"
                tx_key = (EntityType.TRANSACTION, tx_id)
                normalized_entities[tx_key] = Entity(
                    type=EntityType.TRANSACTION,
                    id=tx_id,
                    properties={
                        "amount": payload.get("amount"),
                        "type": payload.get("type"),
                        "step": payload.get("step")
                    }
                )

                # Connect Case -> INVOLVES -> Transaction
                normalized_relationships.append(
                    Relationship(
                        source_type=EntityType.CASE,
                        source_id=case_id,
                        target_type=EntityType.TRANSACTION,
                        target_id=tx_id,
                        type=RelationshipType.INVOLVES
                    )
                )

                # Sender / Receiver accounts (if explicitly named, otherwise use placeholders)
                sender_acc = payload.get("sender_account") or payload.get("origin_account")
                if sender_acc:
                    norm_s = normalize_bank_account(sender_acc)
                    sender_key = (EntityType.BANK_ACCOUNT, norm_s)
                    normalized_entities[sender_key] = Entity(type=EntityType.BANK_ACCOUNT, id=norm_s)
                    
                    # Sender -> USED -> Transaction
                    normalized_relationships.append(
                        Relationship(
                            source_type=EntityType.BANK_ACCOUNT,
                            source_id=norm_s,
                            target_type=EntityType.TRANSACTION,
                            target_id=tx_id,
                            type=RelationshipType.USED
                        )
                    )

                dest_acc = payload.get("receiver_account") or payload.get("destination_account")
                if dest_acc:
                    norm_d = normalize_bank_account(dest_acc)
                    dest_key = (EntityType.BANK_ACCOUNT, norm_d)
                    normalized_entities[dest_key] = Entity(type=EntityType.BANK_ACCOUNT, id=norm_d)
                    
                    # Transaction -> TRANSFERRED_TO -> Destination Account
                    normalized_relationships.append(
                        Relationship(
                            source_type=EntityType.TRANSACTION,
                            source_id=tx_id,
                            target_type=EntityType.BANK_ACCOUNT,
                            target_id=norm_d,
                            type=RelationshipType.TRANSFERRED_TO
                        )
                    )

                upi_id = payload.get("upi_id")
                if upi_id:
                    norm_upi = normalize_upi(upi_id)
                    upi_key = (EntityType.UPI, norm_upi)
                    normalized_entities[upi_key] = Entity(type=EntityType.UPI, id=norm_upi)
                    
                    # Transaction -> CONNECTED_TO -> UPI
                    normalized_relationships.append(
                        Relationship(
                            source_type=EntityType.TRANSACTION,
                            source_id=tx_id,
                            target_type=EntityType.UPI,
                            target_id=norm_upi,
                            type=RelationshipType.CONNECTED_TO
                        )
                    )

                device_id = payload.get("device_id")
                if device_id:
                    norm_dev = normalize_device(device_id)
                    dev_key = (EntityType.DEVICE, norm_dev)
                    normalized_entities[dev_key] = Entity(type=EntityType.DEVICE, id=norm_dev)
                    
                    # Transaction -> USED -> Device
                    normalized_relationships.append(
                        Relationship(
                            source_type=EntityType.TRANSACTION,
                            source_id=tx_id,
                            target_type=EntityType.DEVICE,
                            target_id=norm_dev,
                            type=RelationshipType.USED
                        )
                    )

    # 5. Connect all non-Case nodes of the current extraction directly to the Case node
    # if they do not already have a direct connection, ensuring a fully connected component.
    for key, entity in normalized_entities.items():
        if key[0] == EntityType.CASE:
            continue
        # Check if this entity has a direct relationship to/from the Case node
        has_direct_case_connection = False
        for rel in normalized_relationships:
            if (rel.source_type == EntityType.CASE and rel.source_id == case_id and rel.target_type == entity.type and rel.target_id == entity.id) or \
               (rel.target_type == EntityType.CASE and rel.target_id == case_id and rel.source_type == entity.type and rel.source_id == entity.id):
                has_direct_case_connection = True
                break
        
        if not has_direct_case_connection:
            normalized_relationships.append(
                Relationship(
                    source_type=EntityType.CASE,
                    source_id=case_id,
                    target_type=entity.type,
                    target_id=entity.id,
                    type=RelationshipType.LINKED_WITH
                )
            )

    return list(normalized_entities.values()), normalized_relationships
