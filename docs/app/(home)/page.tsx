import Link from "next/link";

export default function HomePage() {
  const completed = [
    "Core architecture",
    "Window management",
    "IPC",
    "Multi-framework support",
    "Dev server integration",
  ];
  const active = [
    { name: "Documentation", p: "80%" },
    { name: "Additional examples", p: "70%" },
  ];
  const next = [
    "Menu API",
    "Dialog API",
    "System tray",
    "Auto-updater",
    "Build tools",
    "CLI",
  ];

  return (
    <div className="min-h-screen bg-black text-white font-sans selection:bg-white selection:text-black antialiased">
      <div className="mx-auto max-w-2xl px-6 py-12">
        {/* Header */}
        <header className="mb-16 flex items-baseline justify-between border-b border-zinc-900 pb-4">
          <div className="flex items-center gap-2">
            <svg
              width="24"
              height="24"
              viewBox="0 0 340 343"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M339.413 47.9191C341.174 13.2955 324.635 -2.56578 289.791 0.336739C285.169 2.42628 280.638 4.91824 276.196 7.81397C261.305 21.5462 257 38.0872 263.281 57.4356C253.707 66.7807 244.418 76.2972 235.411 85.985C227.416 80.6259 218.806 76.773 209.581 74.4293C170.37 67.6413 141.141 81.4633 121.893 115.894C120.22 116.72 118.408 117.173 116.455 117.253C104.305 114.613 92.297 111.44 80.4286 107.737C77.9312 92.9918 70.227 81.8888 57.3172 74.4293C32.9686 66.2818 14.6154 73.3063 2.2576 95.5015C-3.64261 116.113 2.02241 132.654 19.2513 145.123C40.144 154.175 58.2702 150.322 73.6311 133.567C87.0208 138.032 100.616 141.658 114.416 144.443C118.217 197.413 146.54 225.509 199.385 228.732C202.571 241.933 205.97 255.074 209.581 268.157C206.034 273.302 202.181 278.287 198.025 283.112C188.572 304.436 192.877 322.336 210.94 336.812C237.411 348.844 257.124 341.819 270.078 315.74C275.531 287.205 264.201 269.532 236.091 262.719C232.031 248.747 228.179 234.699 224.535 220.575C230.532 215.518 236.877 210.76 243.568 206.3C247.898 202.38 251.75 198.074 255.124 193.385C272.493 163.524 272.266 133.842 254.444 104.338C264.207 94.3486 274.176 84.6051 284.353 75.109C311.861 84.5263 330.214 75.4625 339.413 47.9191Z"
                fill="white"
              />
              <path
                d="M189.188 98.2202C230.034 103.049 246.575 125.708 238.809 166.195C225.807 192.519 204.735 202.715 175.593 196.784C147.74 183.9 137.089 162.373 143.645 132.208C152.545 112.174 167.727 100.845 189.188 98.2202Z"
                fill="black"
              />
              <path
                d="M182.39 126.77C208.961 125.111 218.251 136.893 210.26 162.117C198.837 173.95 186.829 174.629 174.233 164.156C164.912 148.954 167.631 136.491 182.39 126.77Z"
                fill="white"
              />
            </svg>
            <span className="text-xs font-bold uppercase tracking-tighter">
              Positron
            </span>
          </div>
          <nav className="flex gap-4 text-[10px] font-medium text-zinc-500 uppercase tracking-widest font-mono">
            <Link href="/docs" className="hover:text-white transition-colors">
              Docs
            </Link>
            <a
              href="https://github.com/tomlin7/Positron"
              className="hover:text-white transition-colors"
            >
              Source
            </a>
          </nav>
        </header>

        {/* Hero */}
        <section className="mb-16">
          <h2 className="mb-4 text-xs font-mono uppercase tracking-widest text-zinc-500">
            Framework
          </h2>
          <p className="text-xl font-light leading-tight text-zinc-400 max-w-lg">
            High-performance desktop apps with{" "}
            <span className="text-white">Python</span> and modern web
            frameworks.{" "}
            <span className="text-white">React • Vue • Svelte • Next.js</span>.
            Fast by design. Minimal by choice.
          </p>
          <div className="mt-8">
            <Link
              href="/docs"
              className="text-xs uppercase tracking-widest border-b border-white pb-1 hover:text-zinc-400 hover:border-zinc-400 transition-all"
            >
              Initialize →
            </Link>
          </div>
        </section>

        {/* Progress */}
        <div className="grid gap-x-12 gap-y-10 sm:grid-cols-2">
          {/* Section: Status */}
          <div className="space-y-8">
            <div>
              <h3 className="mb-3 text-[10px] uppercase tracking-[0.3em] text-zinc-500">
                01. Finished
              </h3>
              <ul className="space-y-1 text-sm font-mono text-zinc-400 italic">
                {completed.map((i) => (
                  <li key={i}>/ {i}</li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="mb-3 text-[10px] uppercase tracking-[0.3em] text-white">
                02. Building
              </h3>
              <div className="space-y-4">
                {active.map((i) => (
                  <div key={i.name}>
                    <div className="flex justify-between text-[11px] uppercase tracking-tighter text-zinc-400 mb-1">
                      <span>{i.name}</span>
                      <span>{i.p}</span>
                    </div>
                    <div className="h-[1px] w-full bg-zinc-900 overflow-hidden">
                      <div
                        className="h-full bg-white transition-all duration-1000"
                        style={{ width: i.p }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Section: Roadmap */}
          <div>
            <h3 className="mb-3 text-[10px] uppercase tracking-[0.3em] text-zinc-600">
              03. Pipeline
            </h3>
            <div className="grid grid-cols-1 gap-1 text-[12px] font-mono text-zinc-700">
              {next.map((i) => (
                <span key={i}>+ {i}</span>
              ))}
            </div>
          </div>
        </div>

        <footer className="mt-24 pt-4 border-t border-zinc-900 flex justify-between items-center text-[9px] text-zinc-800 uppercase tracking-[0.3em]">
          <span>Positron Core v1.0.0-alpha</span>
          <span>2024</span>
        </footer>
      </div>
    </div>
  );
}
