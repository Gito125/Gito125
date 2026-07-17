<svg width="1000" height="420" viewBox="0 0 1000 420" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .term-bg { fill: #0d1117; }
      .titlebar { fill: #161b22; }
      .dot-red { fill: #ff5f56; }
      .dot-amber { fill: #ffbd2e; }
      .dot-green { fill: #27c93f; }
      .path { fill: #8b949e; font: 500 13px 'SF Mono', 'Fira Code', monospace; }
      .prompt-user { fill: #58a6ff; font: 600 15px 'Fira Code', monospace; }
      .prompt-sep { fill: #8b949e; font: 600 15px 'Fira Code', monospace; }
      .prompt-dir { fill: #d29922; font: 600 15px 'Fira Code', monospace; }
      .cmd { fill: #c9d1d9; font: 15px 'Fira Code', monospace; }
      .comment { fill: #6e7681; font: 13px 'Fira Code', monospace; }
      .out-key { fill: #79c0ff; font: 14px 'Fira Code', monospace; }
      .out-str { fill: #a5d6ff; font: 13px 'Fira Code', monospace; }
      .stmt { fill: #f0f6fc; font: 700 25px 'Fira Code', monospace; }
      .stmt-accent { fill: #58a6ff; font: 700 25px 'Fira Code', monospace; }
      .cursor { fill: #58a6ff; }
    </style>
    <clipPath id="term-clip">
      <rect x="0" y="0" width="1000" height="420" rx="12" ry="12"/>
    </clipPath>
  </defs>

  <g clip-path="url(#term-clip)">
    <rect class="term-bg" x="0" y="0" width="1000" height="420"/>

    <!-- title bar -->
    <rect class="titlebar" x="0" y="0" width="1000" height="36"/>
    <circle class="dot-red" cx="22" cy="18" r="6.5"/>
    <circle class="dot-amber" cx="44" cy="18" r="6.5"/>
    <circle class="dot-green" cx="66" cy="18" r="6.5"/>
    <text class="path" x="500" y="22.5" text-anchor="middle">gideon@kampala: ~/ogwang-gift-gideon</text>

    <!-- ===== Line 1: whoami ===== -->
    <g opacity="0">
      <text class="prompt-user" x="24" y="70">gideon</text>
      <text class="prompt-sep" x="86" y="70">@kampala</text>
      <text class="prompt-dir" x="168" y="70">~</text>
      <text class="prompt-sep" x="182" y="70">$</text>
      <text class="cmd" x="198" y="70">whoami --role</text>
      <animate attributeName="opacity" from="0" to="1" begin="0.1s" dur="0.1s" fill="freeze"/>
    </g>
    <g opacity="0">
      <text class="out-str" x="24" y="98">&gt; Full-stack developer building the</text>
      <text class="out-str" x="24" y="118">&gt; operating layer for African institutions.</text>
      <animate attributeName="opacity" from="0" to="1" begin="0.9s" dur="0.3s" fill="freeze"/>
    </g>

    <!-- ===== Line 2: ls currently-building ===== -->
    <g opacity="0">
      <text class="prompt-user" x="24" y="154">gideon</text>
      <text class="prompt-sep" x="86" y="154">@kampala</text>
      <text class="prompt-dir" x="168" y="154">~</text>
      <text class="prompt-sep" x="182" y="154">$</text>
      <text class="cmd" x="198" y="154">ls --currently-building</text>
      <animate attributeName="opacity" from="0" to="1" begin="1.3s" dur="0.1s" fill="freeze"/>
    </g>
    <g opacity="0">
      <text class="out-key" x="24" y="180">drwx  Acadex</text>
      <text class="comment" x="200" y="180"># multi-tenant school SaaS, Uganda-first</text>
      <text class="out-key" x="24" y="202">drwx  RestaurantOS</text>
      <text class="comment" x="240" y="202"># ordering, kitchen &amp; staff ops in one system</text>
      <animate attributeName="opacity" from="0" to="1" begin="2.1s" dur="0.3s" fill="freeze"/>
    </g>

    <!-- ===== Line 3: stack ===== -->
    <g opacity="0">
      <text class="prompt-user" x="24" y="238">gideon</text>
      <text class="prompt-sep" x="86" y="238">@kampala</text>
      <text class="prompt-dir" x="168" y="238">~</text>
      <text class="prompt-sep" x="182" y="238">$</text>
      <text class="cmd" x="198" y="238">cat stack.json</text>
      <animate attributeName="opacity" from="0" to="1" begin="2.6s" dur="0.1s" fill="freeze"/>
    </g>
    <g opacity="0">
      <text class="out-str" x="24" y="264">[TypeScript, Python, Next.js, React, Tailwind CSS,</text>
      <text class="out-str" x="24" y="282">Node.js, Prisma, PostgreSQL]</text>
      <animate attributeName="opacity" from="0" to="1" begin="3.3s" dur="0.3s" fill="freeze"/>
    </g>

    <!-- ===== Final: the statement ===== -->
    <g opacity="0">
      <text class="prompt-user" x="24" y="318">gideon</text>
      <text class="prompt-sep" x="86" y="318">@kampala</text>
      <text class="prompt-dir" x="168" y="318">~</text>
      <text class="prompt-sep" x="182" y="318">$</text>
      <text class="cmd" x="198" y="318">./ship.sh --no-excuses</text>
      <animate attributeName="opacity" from="0" to="1" begin="3.8s" dur="0.1s" fill="freeze"/>
    </g>

    <g opacity="0">
      <text class="stmt" x="24" y="360">I build systems that run</text>
      <text class="stmt-accent" x="24" y="392">institutions while the world sleeps.</text>
      <animate attributeName="opacity" from="0" to="1" begin="4.5s" dur="0.5s" fill="freeze"/>
    </g>

    <g opacity="0">
      <rect class="cursor" x="640" y="380" width="11" height="18">
        <animate attributeName="opacity" values="1;0;1" dur="1s" begin="5s" repeatCount="indefinite"/>
      </rect>
      <animate attributeName="opacity" from="0" to="1" begin="5s" dur="0.1s" fill="freeze"/>
    </g>
  </g>

  <rect x="0.5" y="0.5" width="999" height="419" rx="12" ry="12" fill="none" stroke="#30363d" stroke-width="1"/>
</svg>
