import Link from "next/link";

export default function HomePage() {
  const completed = ["Core architecture", "Window management", "IPC", "React + Vite"];
  const current = ["Documentation (75%)", "Examples (60%)"];
  const next = ["Menu API", "Dialog API", "System tray", "Auto-updater", "Build tools", "CLI"];

  return (
    <div className="min-h-screen bg-black text-white font-sans selection:bg-white selection:text-black">
      <div className="mx-auto max-w-2xl px-6 py-20">
        {/* Header */}
        <header className="mb-12 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <svg
              width="32"
              height="32"
              viewBox="0 0 340 343"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              className="opacity-90 grayscale"
            >
              <path fillRule="evenodd" clipRule="evenodd" d="M339.413 47.9191C341.174 13.2955 324.635 -2.56578 289.791 0.336739C285.169 2.42628 280.638 4.91824 276.196 7.81397C261.305 21.5462 257 38.0872 263.281 57.4356C253.707 66.7807 244.418 76.2972 235.411 85.985C227.416 80.6259 218.806 76.773 209.581 74.4293C170.37 67.6413 141.141 81.4633 121.893 115.894C120.22 116.72 118.408 117.173 116.455 117.253C104.305 114.613 92.297 111.44 80.4286 107.737C77.9312 92.9918 70.227 81.8888 57.3172 74.4293C32.9686 66.2818 14.6154 73.3063 2.2576 95.5015C-3.64261 116.113 2.02241 132.654 19.2513 145.123C40.144 154.175 58.2702 150.322 73.6311 133.567C87.0208 138.032 100.616 141.658 114.416 144.443C118.217 197.413 146.54 225.509 199.385 228.732C202.571 241.933 205.97 255.074 209.581 268.157C206.034 273.302 202.181 278.287 198.025 283.112C188.572 304.436 192.877 322.336 210.94 336.812C237.411 348.844 257.124 341.819 270.078 315.74C275.531 287.205 264.201 269.532 236.091 262.719C232.031 248.747 228.179 234.699 224.535 220.575C230.532 215.518 236.877 210.76 243.568 206.3C247.898 202.38 251.75 198.074 255.124 193.385C272.493 163.524 272.266 133.842 254.444 104.338C264.207 94.3486 274.176 84.6051 284.353 75.109C311.861 84.5263 330.214 75.4625 339.413 47.9191Z" fill="white" />
              <path fillRule="evenodd" clipRule="evenodd" d="M189.188 98.2202C230.034 103.049 246.575 125.708 238.809 166.195C225.807 192.519 204.735 202.715 175.593 196.784C147.74 183.9 137.089 162.373 143.645 132.208C152.545 112.174 167.727 100.845 189.188 98.2202Z" fill="black" />
              <path fillRule="evenodd" clipRule="evenodd" d="M182.39 126.77C208.961 125.111 218.251 136.893 210.260 162.117C198.837 173.95 186.829 174.629 174.233 164.156C164.912 148.954 167.631 136.491 182.390 126.77Z" fill="white" />
            </svg>
            <h1 className="text-xl font-bold tracking-tighter uppercase">Positron</h1>
          </div>
          <nav className="flex gap-6 text-sm font-medium text-zinc-500 uppercase tracking-widest">
            <Link href="/docs" className="hover:text-white transition-colors">Docs</Link>
            <a href="https://github.com/tomlin7/Positron" className="hover:text-white transition-colors">GitHub</a>
          </nav>
        </header>

        {/* Hero */}
        <section className="mb-20">
          <p className="text-2xl font-light leading-relaxed text-zinc-400">
            A high-performance framework for building desktop applications with
            <span className="text-white"> Python</span> and
            <span className="text-white"> React</span>.
            No Node.js. Pure speed.
          </p>
        </section>

        {/* Progress System */}
        <section className="space-y-12">
          <div>
            <div className="mb-4 flex items-center gap-2">
              <span className="text-[10px] uppercase tracking-[0.2em] text-zinc-500">01 / Done</span>
              <div className="h-px flex-1 bg-zinc-800" />
            </div>
            <div className="grid grid-cols-2 gap-y-2 text-sm text-zinc-400">
              {completed.map((item) => (
                <div key={item} className="flex items-center gap-2">
                  <span className="h-1 w-1 bg-zinc-600" />
                  {item}
                </div>
              ))}
            </div>
          </div>

          <div>
            <div className="mb-4 flex items-center gap-2">
              <span className="text-[10px] uppercase tracking-[0.2em] text-white">02 / Active</span>
              <div className="h-px flex-1 bg-zinc-800" />
            </div>
            <div className="space-y-3">
              {current.map((item) => (
                <div key={item} className="group relative">
                  <div className="flex justify-between text-sm mb-1 text-white uppercase tracking-tight">
                    <span>{item.split(" (")[0]}</span>
                    <span className="text-zinc-500">{item.match(/\(([^)]+)\)/)?.[1]}</span>
                  </div>
                  <div className="h-[1px] w-full bg-zinc-900 overflow-hidden">
                    <div
                      className="h-full bg-white"
                      style={{ width: item.includes("75") ? "75%" : "60%" }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div>
            <div className="mb-4 flex items-center gap-2">
              <span className="text-[10px] uppercase tracking-[0.2em] text-zinc-500">03 / Next</span>
              <div className="h-px flex-1 bg-zinc-800" />
            </div>
            <div className="grid grid-cols-3 gap-4 text-[13px] text-zinc-600 italic">
              {next.map((item) => (
                <span key={item}>{item}</span>
              ))}
            </div>
          </div>
        </section>

        <footer className="mt-32 pt-8 border-t border-zinc-900 text-[10px] text-zinc-700 uppercase tracking-widest flex justify-between">
          <span>Built for the future of desktop</span>
          <span>© 2024</span>
        </footer>
      </div>
    </div>
  );
}
