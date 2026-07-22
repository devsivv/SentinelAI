import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import { UserCheck, Server, Layout } from 'lucide-react';

const teamMembers = [
  {
    name: 'Shivam Dubey',
    role: 'Team Leader',
    focus: 'Backend, AI & Architecture',
    bio: 'Architected the multi-agent AI orchestration pipeline, FastAPI backend, PostgreSQL schema, and model inference services.',
    icon: Server,
    tags: ['FastAPI', 'PyTorch', 'System Architecture', 'SHAP Explainability'],
  },
  {
    name: 'Ankit Yadav',
    role: 'Frontend Lead',
    focus: 'UI/UX & Integration',
    bio: 'Designed and built the Citizen Portal, Police Dashboard, and SentinelAI Landing Page with modern responsive aesthetics.',
    icon: Layout,
    tags: ['React', 'TypeScript', 'Tailwind CSS', 'Vite & Recharts'],
  },
];

export default function TeamSection() {
  const ref = useRef<HTMLElement>(null);
  const inView = useInView(ref, { once: true, margin: '-60px' });

  return (
    <section
      id="team"
      ref={ref}
      className="py-24 sm:py-32 px-4 sm:px-6 lg:px-8 relative"
      aria-labelledby="team-heading"
    >
      <div className="mx-auto max-w-7xl relative">
        {/* Heading */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="text-center mb-16 sm:mb-20"
        >
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-300 text-xs font-semibold uppercase tracking-wider mb-4">
            <UserCheck className="h-3.5 w-3.5" aria-hidden="true" />
            Team Riyal Intelligence
          </div>
          <h2
            id="team-heading"
            className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight"
          >
            Meet the Builders
          </h2>
          <p className="mt-4 text-gray-400 text-base max-w-xl mx-auto">
            Built by Team Riyal Intelligence during the ET AI Hackathon.
          </p>
          <div className="mt-5 mx-auto w-16 h-0.5 bg-gradient-to-r from-transparent via-blue-500 to-transparent rounded-full" aria-hidden="true" />
        </motion.div>

        {/* Team Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {teamMembers.map((member, idx) => (
            <motion.div
              key={member.name}
              initial={{ opacity: 0, y: 28 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.55, delay: idx * 0.15 }}
            >
              <motion.div
                whileHover={{ y: -4, boxShadow: '0 0 32px rgba(37,99,235,0.18)' }}
                transition={{ type: 'spring', stiffness: 280, damping: 20 }}
                className="glass-card p-8 flex flex-col h-full relative"
              >
                <div className="flex items-center gap-4 mb-6">
                  <div className="w-14 h-14 rounded-2xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400 shrink-0">
                    <member.icon className="h-7 w-7" aria-hidden="true" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-white">{member.name}</h3>
                    <p className="text-sm font-semibold text-blue-400">{member.role}</p>
                    <p className="text-xs text-gray-400">{member.focus}</p>
                  </div>
                </div>

                <p className="text-sm text-gray-300 leading-relaxed mb-6 flex-1">
                  {member.bio}
                </p>

                {/* Skill tags */}
                <div className="flex flex-wrap gap-2 pt-4 border-t border-gray-800">
                  {member.tags.map((tag) => (
                    <span
                      key={tag}
                      className="text-xs font-medium px-2.5 py-1 rounded-md bg-blue-950/60 border border-blue-800/40 text-blue-300"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </motion.div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
