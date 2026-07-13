export default function Home() {
  return (
    <div className="text-center mt-20">
      <h2 className="text-4xl font-extrabold text-gray-900 sm:text-5xl">
        Welcome to SentinelAI
      </h2>
      <p className="mt-4 text-lg text-gray-500">
        AI-powered cybercrime detection platform.
      </p>
      <div className="mt-8">
        <a href="/investigate" className="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
          Start Investigation
        </a>
      </div>
    </div>
  );
}
