import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';

const tech = [
  { label: 'React', category: 'Frontend' },
  { label: 'TypeScript', category: 'Frontend' },
  { label: 'Tailwind CSS', category: 'Frontend' },
  { label: 'Vite', category: 'Frontend' },
  { label: 'FastAPI', category: 'Backend' },
  { label: 'Python 3.14', category: 'Backend' },
  { label: 'PostgreSQL', category: 'Backend' },
  { label: 'Alembic', category: 'Backend' },
  { label: 'XGBoost', category: 'AI/ML' },
  { label: 'Scikit-Learn', category: 'AI/ML' },
  { label: 'PyTorch', category: 'AI/ML' },
  { label: 'SHAP', category: 'AI/ML' },
  { label: 'Transformers', category: 'AI/ML' },
  { label: 'Render', category: 'Infrastructure' },
  { label: 'Vercel', category: 'Infrastructure' },
  { label: 'Neon DB', category: 'Infrastructure' },
  { label: 'GitHub', category: 'Infrastructure' },
];

const categoryColor: Record<string, string> = {
  Frontend: 'border-blue-600/40 bg-blue-600/10 text-blue-300 hover:border-blue-400/60 hover:bg-blue-600/20',
  Backend: 'border-green-600/40 bg-green-600/10 text-green-300 hover:border-green-400/60 hover:bg-green-600/20',
  'AI/ML': 'border-purple-600/40 bg-purple-600/10 text-purple-300 hover:border-purple-400/60 hover:bg-purple-600/20',
  Infrastructure: 'border-amber-600/40 bg-amber-600/10 text-amber-300 hover:border-amber-400/60 hover:bg-amber-600/20',
};

const categories = ['Frontend', 'Backend', 'AI/ML', 'Infrastructure'];
const categoryLabelColor: Record<string, string> = {
  Frontend: 'text-blue-400',
  Backend: 'text-green-400',
  'AI/ML': 'text-purple-400',
  Infrastructure: 'text-amber-400',
};

export default function TechStackSection() {
  const ref = useRef<HTMLElement>(null);
  const inView = useInView(ref, { once: true, margin: '-60px' });

  return (
    <section
      id="tech-stack"
      ref={ref}
      className="py-24 sm:py-32 px-4 sm:px-6 lg:px-8"
      aria-labelledby="tech-heading"
    >
      <div className="mx-auto max-w-5xl">
        {/* Heading */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="text-center mb-14"
        >
          <p className="text-blue-400 font-semibold text-sm tracking-widest uppercase mb-3">Technology Stack</p>
          <h2
            id="tech-heading"
            className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight"
          >
            Enterprise-Grade Technologies
          </h2>
          <div className="mt-5 mx-auto w-16 h-0.5 bg-gradient-to-r from-transparent via-blue-500 to-transparent rounded-full" aria-hidden="true" />
        </motion.div>

        {/* By category */}
        <div className="space-y-8">
          {categories.map((cat, catIdx) => (
            <motion.div
              key={cat}
              initial={{ opacity: 0, x: -16 }}
              animate={inView ? { opacity: 1, x: 0 } : {}}
              transition={{ duration: 0.5, delay: catIdx * 0.08 }}
              className="flex flex-col sm:flex-row sm:items-start gap-3 sm:gap-6"
            >
              <div className="shrink-0 w-28">
                <span className={`text-xs font-bold uppercase tracking-widest ${categoryLabelColor[cat]}`}>
                  {cat}
                </span>
              </div>
              <div className="flex flex-wrap gap-2.5">
                {tech
                  .filter((t) => t.category === cat)
                  .map((t, i) => (
                    <motion.span
                      key={t.label}
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={inView ? { opacity: 1, scale: 1 } : {}}
                      transition={{ duration: 0.35, delay: catIdx * 0.08 + i * 0.04 }}
                      whileHover={{ scale: 1.06, y: -2 }}
                      className={`inline-flex items-center px-4 py-1.5 rounded-full text-sm font-semibold border transition-all duration-200 cursor-default ${categoryColor[cat]}`}
                    >
                      {t.label}
                    </motion.span>
                  ))}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
