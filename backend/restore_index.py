
import os

file_path = r"e:\Anti-Lust app\website\index.html"

full_content = """<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>Anti-Lust Guardian | Orbital Defense System</title>
    <meta name="description"
        content="Advanced AI-powered content filtering and parental controls. The ultimate defense for your digital frontier." />
    <meta name="theme-color" content="#030014" />

    <!-- Fonts: Orbitron (Headers) & Rajdhani (Body) -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap"
        rel="stylesheet">

    <style>
        :root {
            --bg-void: #000000;
            --neon-cyan: #00F3FF;
            --neon-purple: #BC13FE;
            --neon-blue: #2E5CFF;
            --glass-border: rgba(255, 255, 255, 0.1);
            --glass-bg: rgba(10, 10, 30, 0.6);
            --text-main: #E0E6ED;
            --text-muted: #94A3B8;
            --success: #00FF94;
            --danger: #FF2A6D;
            --font-head: 'Orbitron', sans-serif;
            --font-body: 'Rajdhani', sans-serif;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            background-color: var(--bg-void);
            color: var(--text-main);
            font-family: var(--font-body);
            overflow-x: hidden;
            line-height: 1.6;
            /* cursor: none; Removed default hiding */
        }

        body.custom-cursor-active {
            cursor: none;
        }

        /* --- Custom Cursor --- */
            position: fixed;
            top: 0;
            left: 0;
            width: 20px;
            height: 20px;
            border: 2px solid var(--neon-cyan);
            border-radius: 50%;
            pointer-events: none;
            z-index: 2147483647; /* Max z-index */
            transform: translate(-50%, -50%);
            transition: width 0.2s, height 0.2s, background 0.2s;
            box-shadow: 0 0 10px var(--neon-cyan);
        }

            width: 50px;
            height: 50px;
            background: rgba(0, 243, 255, 0.1);
            border-color: var(--neon-purple);
            box-shadow: 0 0 20px var(--neon-purple);
        }

            position: fixed;
            top: 0;
            left: 0;
            width: 6px;
            height: 6px;
            background: #fff;
            border-radius: 50%;
            pointer-events: none;
            z-index: 2147483647;
            transform: translate(-50%, -50%);
            box-shadow: 0 0 10px #fff;
        }

        /* --- Backgrounds --- */
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -2;
        }

            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(to bottom, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0) 50%, rgba(0, 0, 0, 0.1) 50%, rgba(0, 0, 0, 0.1));
            background-size: 100% 4px;
            z-index: 999;
            pointer-events: none;
            opacity: 0.2;
        }

            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            /* Adjusted vignette to be less aggressive */
            background: radial-gradient(circle, transparent 75%, #000000 100%);
            z-index: 998;
            pointer-events: none;
        }

        /* --- Typography & Utilities --- */
        h1,
        h2,
        h3,
        h4 {
            font-family: var(--font-head);
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .text-gradient {
            background: linear-gradient(90deg, var(--neon-cyan), var(--neon-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 24px;
            position: relative;
            z-index: 10;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 16px 32px;
            font-family: var(--font-head);
            font-weight: 700;
            font-size: 14px;
            letter-spacing: 1px;
            text-decoration: none;
            color: var(--neon-cyan);
            background: rgba(0, 243, 255, 0.05);
            border: 1px solid var(--neon-cyan);
            clip-path: polygon(10% 0, 100% 0, 100% 70%, 90% 100%, 0 100%, 0 30%);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 243, 255, 0.4), transparent);
            transition: 0.5s;
        }

        .btn:hover::before {
            left: 100%;
        }

        .btn:hover {
            background: rgba(0, 243, 255, 0.15);
            box-shadow: 0 0 20px rgba(0, 243, 255, 0.4);
            text-shadow: 0 0 8px var(--neon-cyan);
            transform: translateY(-2px);
        }

        .btn-primary {
            background: var(--neon-cyan);
            color: #000;
            border: none;
        }

        .btn-primary:hover {
            background: #fff;
            box-shadow: 0 0 30px var(--neon-cyan);
        }

        /* --- Header --- */
        header {
            position: fixed;
            top: 0;
            width: 100%;
            z-index: 100;
            padding: 20px 0;
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.3s;
        }

        header.scrolled {
            background: rgba(3, 0, 20, 0.9);
            padding: 10px 0;
        }

        .nav-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            font-family: var(--font-head);
            font-weight: 900;
            font-size: 24px;
            color: #fff;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .logo span {
            color: var(--neon-cyan);
        }

        nav ul {
            display: flex;
            gap: 30px;
            list-style: none;
        }

        nav a {
            color: var(--text-muted);
            text-decoration: none;
            font-weight: 500;
            font-size: 16px;
            transition: color 0.3s;
            position: relative;
        }

        nav a:hover {
            color: var(--neon-cyan);
        }

        nav a::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 0;
            height: 2px;
            background: var(--neon-cyan);
            transition: width 0.3s;
        }

        nav a:hover::after {
            width: 100%;
        }

        /* --- Hero Section --- */
        .hero {
            min-height: 100vh;
            display: flex;
            align-items: center;
            padding-top: 80px;
            position: relative;
        }

        .hero-grid {
            display: grid;
            grid-template-columns: 1.2fr 0.8fr;
            gap: 50px;
            align-items: center;
        }

        .hero-content h1 {
            font-size: 64px;
            line-height: 1.1;
            margin-bottom: 24px;
            text-shadow: 0 0 20px rgba(0, 243, 255, 0.3);
        }

        .hero-content p {
            font-size: 20px;
            color: var(--text-muted);
            margin-bottom: 40px;
            max-width: 600px;
        }

        .glitch {
            position: relative;
        }

        .glitch::before,
        .glitch::after {
            content: attr(data-text);
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }

        .glitch::before {
            left: 2px;
            text-shadow: -1px 0 var(--danger);
            clip: rect(44px, 450px, 56px, 0);
            animation: glitch-anim 5s infinite linear alternate-reverse;
        }

        .glitch::after {
            left: -2px;
            text-shadow: -1px 0 var(--neon-blue);
            clip: rect(44px, 450px, 56px, 0);
            animation: glitch-anim2 5s infinite linear alternate-reverse;
        }

        @keyframes glitch-anim {
            0% {
                clip: rect(14px, 9999px, 127px, 0);
            }

            5% {
                clip: rect(81px, 9999px, 11px, 0);
            }

            10% {
                clip: rect(109px, 9999px, 73px, 0);
            }

            15% {
                clip: rect(2px, 9999px, 16px, 0);
            }

            20% {
                clip: rect(56px, 9999px, 88px, 0);
            }

            100% {
                clip: rect(16px, 9999px, 119px, 0);
            }
        }

        @keyframes glitch-anim2 {
            0% {
                clip: rect(126px, 9999px, 12px, 0);
            }

            5% {
                clip: rect(32px, 9999px, 95px, 0);
            }

            10% {
                clip: rect(109px, 9999px, 12px, 0);
            }

            15% {
                clip: rect(138px, 9999px, 114px, 0);
            }

            20% {
                clip: rect(53px, 9999px, 32px, 0);
            }

            100% {
                clip: rect(67px, 9999px, 122px, 0);
            }
        }

        /* 3D Shield Animation */
        .shield-container {
            position: relative;
            width: 400px;
            height: 400px;
            perspective: 1000px;
            margin: 0 auto;
        }

        .shield {
            width: 100%;
            height: 100%;
            position: relative;
            transform-style: preserve-3d;
            animation: rotate 10s infinite linear;
        }

        .shield-ring {
            position: absolute;
            top: 50%;
            left: 50%;
            border: 2px solid var(--neon-cyan);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            box-shadow: 0 0 20px var(--neon-cyan);
        }

        .r1 {
            width: 300px;
            height: 300px;
            border-style: dashed;
            animation: spin 10s infinite linear;
        }

        .r2 {
            width: 240px;
            height: 240px;
            border-color: var(--neon-purple);
            animation: spin-rev 8s infinite linear;
        }

        .r3 {
            width: 180px;
            height: 180px;
            border-width: 4px;
            animation: spin 6s infinite linear;
        }

        .core {
            position: absolute;
            top: 50%;
            left: 50%;
            width: 100px;
            height: 100px;
            background: radial-gradient(circle, var(--neon-cyan), transparent);
            transform: translate(-50%, -50%);
            border-radius: 50%;
            filter: blur(20px);
            animation: pulse 2s infinite ease-in-out;
        }

        @keyframes rotate {
            0% {
                transform: rotateY(0deg);
            }

            100% {
                transform: rotateY(360deg);
            }
        }

        @keyframes spin {
            0% {
                transform: translate(-50%, -50%) rotate(0deg);
            }

            100% {
                transform: translate(-50%, -50%) rotate(360deg);
            }
        }

        @keyframes spin-rev {
            0% {
                transform: translate(-50%, -50%) rotate(0deg);
            }

            100% {
                transform: translate(-50%, -50%) rotate(-360deg);
            }
        }

        @keyframes pulse {

            0%,
            100% {
                transform: translate(-50%, -50%) scale(1);
                opacity: 0.8;
            }

            50% {
                transform: translate(-50%, -50%) scale(1.2);
                opacity: 1;
            }
        }

        /* --- Stats Ticker --- */
        .ticker-wrap {
            position: absolute;
            bottom: 0;
            width: 100%;
            background: rgba(0, 243, 255, 0.05);
            border-top: 1px solid rgba(0, 243, 255, 0.2);
            border-bottom: 1px solid rgba(0, 243, 255, 0.2);
            overflow: hidden;
            height: 50px;
            display: flex;
            align-items: center;
        }

        .ticker {
            display: flex;
            animation: ticker 20s infinite linear;
        }

        .ticker-item {
            padding: 0 40px;
            font-family: var(--font-head);
            color: var(--neon-cyan);
            font-size: 14px;
            white-space: nowrap;
        }

        @keyframes ticker {
            0% {
                transform: translateX(0);
            }

            100% {
                transform: translateX(-100%);
            }
        }

        /* --- Features --- */
        .section {
            padding: 120px 0;
        }

        .section-header {
            text-align: center;
            margin-bottom: 80px;
        }

        .section-header h2 {
            font-size: 42px;
            margin-bottom: 16px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
        }

        .card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--glass-border);
            padding: 40px;
            position: relative;
            overflow: hidden;
            transition: all 0.4s;
            backdrop-filter: blur(10px);
        }

        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
            transform: scaleX(0);
            transition: transform 0.4s;
        }

        .card:hover {
            transform: translateY(-10px);
            background: rgba(255, 255, 255, 0.05);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
            border-color: var(--neon-cyan);
        }

        .card:hover::before {
            transform: scaleX(1);
        }

        .card-icon {
            font-size: 40px;
            margin-bottom: 24px;
            color: var(--neon-cyan);
        }

        .card h3 {
            font-size: 24px;
            margin-bottom: 16px;
            color: #fff;
        }

        .card p {
            color: var(--text-muted);
        }

        /* --- Pricing --- */
        .pricing-toggle {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 60px;
            align-items: center;
        }

        .toggle-label {
            font-family: var(--font-head);
            font-weight: 700;
            color: var(--text-muted);
            transition: color 0.3s;
        }

        .toggle-label.active {
            color: #fff;
            text-shadow: 0 0 10px var(--neon-cyan);
        }

        .switch {
            position: relative;
            display: inline-block;
            width: 60px;
            height: 34px;
        }

        .switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }

        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(255, 255, 255, 0.1);
            transition: .4s;
            border-radius: 34px;
            border: 1px solid var(--glass-border);
        }

        .slider:before {
            position: absolute;
            content: "";
            height: 26px;
            width: 26px;
            left: 4px;
            bottom: 3px;
            background-color: var(--neon-cyan);
            transition: .4s;
            border-radius: 50%;
            box-shadow: 0 0 10px var(--neon-cyan);
        }

        input:checked+.slider {
            background-color: rgba(188, 19, 254, 0.2);
            border-color: var(--neon-purple);
        }

        input:checked+.slider:before {
            transform: translateX(26px);
            background-color: var(--neon-purple);
            box-shadow: 0 0 10px var(--neon-purple);
        }

        .pricing-card {
            border: 1px solid var(--glass-border);
            background: rgba(10, 10, 20, 0.6);
            padding: 50px;
            text-align: center;
            position: relative;
            transition: all 0.4s;
        }

        .pricing-card.featured {
            border-color: var(--neon-purple);
            box-shadow: 0 0 30px rgba(188, 19, 254, 0.1);
        }

        .pricing-card:hover {
            transform: scale(1.03);
            z-index: 2;
        }

        .price-amount {
            font-size: 64px;
            font-family: var(--font-head);
            font-weight: 900;
            margin: 20px 0;
            color: #fff;
        }

        .price-period {
            font-size: 18px;
            color: var(--text-muted);
        }

        .features-list {
            list-style: none;
            margin: 40px 0;
            text-align: left;
        }

        .features-list li {
            padding: 12px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .features-list li::before {
            content: '>';
            color: var(--neon-cyan);
            font-family: var(--font-head);
            font-weight: 900;
        }

        /* --- Footer --- */
        footer {
            border-top: 1px solid var(--glass-border);
            padding: 80px 0 40px;
            background: rgba(0, 0, 0, 0.8);
            position: relative;
            z-index: 10;
        }

        .footer-grid {
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr;
            gap: 40px;
            margin-bottom: 60px;
        }

        .footer-col h4 {
            color: #fff;
            margin-bottom: 24px;
        }

        .footer-col ul {
            list-style: none;
        }

        .footer-col ul li {
            margin-bottom: 12px;
        }

        .footer-col a {
            color: var(--text-muted);
            text-decoration: none;
            transition: color 0.3s;
        }

        .footer-col a:hover {
            color: var(--neon-cyan);
        }

        .copyright {
            text-align: center;
            padding-top: 40px;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            color: var(--text-muted);
            font-size: 14px;
        }

        /* --- Mobile --- */
        @media (max-width: 968px) {
            .hero-grid {
                grid-template-columns: 1fr;
                text-align: center;
            }

            .hero-content h1 {
                font-size: 42px;
            }

            .shield-container {
                width: 300px;
                height: 300px;
                margin: 40px auto;
            }

            .footer-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>

<body>
    <!-- Background Layers -->
    <canvas id="starfield"></canvas>
    <div id="scanlines"></div>
    <div id="vignette"></div>
    
    <!-- Custom Cursor Elements -->
    <div id="cursor"></div>
    <div id="cursor-dot"></div>

    <!-- Header -->
    <header id="header">
        <div class="container nav-container">
            <a href="#" class="logo"><span>🛡️</span> ANTI-LUST GUARDIAN</a>
            <nav>
                <ul>
                    <li><a href="#features">MODULES</a></li>
                    <li><a href="#demo">SIMULATION</a></li>
                    <li><a href="#download">DEPLOY</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="hero">
        <div class="container hero-grid">
            <div class="hero-content">
                <h4 style="color: var(--neon-cyan); margin-bottom: 16px;">SYSTEM STATUS: ACTIVE</h4>
                <h1 class="glitch" data-text="ADVANCED AI DEFENSE MATRIX">ADVANCED AI DEFENSE MATRIX</h1>
                <p>Deploy military-grade content filtering and behavioral analysis. Protect your digital frontier with
                    the world's most advanced neural network guardian.</p>
                <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                    <a href="#download" class="btn btn-primary">INITIATE PROTOCOL</a>
                    <a href="#demo" class="btn">VIEW DEMO</a>
                </div>
            </div>

            <div class="shield-container">
                <div class="shield">
                    <div class="shield-ring r1"></div>
                    <div class="shield-ring r2"></div>
                    <div class="shield-ring r3"></div>
                    <div class="core"></div>
                </div>
            </div>
        </div>

        <div class="ticker-wrap">
            <div class="ticker">
                <div class="ticker-item">THREAT DETECTED: 104.23.11.55 [BLOCKED]</div>
                <div class="ticker-item">SYSTEM INTEGRITY: 100%</div>
                <div class="ticker-item">NEW DEVICE PAIRED: IPHONE-15-PRO</div>
                <div class="ticker-item">AI MODEL UPDATED: V4.2.0</div>
                <div class="ticker-item">THREAT DETECTED: 192.168.1.105 [BLOCKED]</div>
                <div class="ticker-item">ENCRYPTION: AES-256 ACTIVE</div>
                <div class="ticker-item">THREAT DETECTED: 104.23.11.55 [BLOCKED]</div>
                <div class="ticker-item">SYSTEM INTEGRITY: 100%</div>
                <div class="ticker-item">NEW DEVICE PAIRED: IPHONE-15-PRO</div>
                <div class="ticker-item">AI MODEL UPDATED: V4.2.0</div>
            </div>
        </div>
    </section>

    <!-- Demo Section -->
    <section id="demo" class="section"
        style="background: linear-gradient(180deg, var(--bg-void) 0%, rgba(0, 243, 255, 0.05) 50%, var(--bg-void) 100%);">
        <div class="container">
            <div class="section-header">
                <h2 class="text-gradient">LIVE THREAT SIMULATION</h2>
                <p style="color: var(--text-muted);">NEURAL ENGINE V4.2.0 // REAL-TIME INTERCEPTION</p>
            </div>

            <div class="shield-container"
                style="width: 100%; max-width: 800px; height: 400px; background: rgba(0, 0, 0, 0.5); border: 1px solid var(--neon-cyan); margin: 0 auto; position: relative; overflow: hidden; border-radius: 4px;">
                <!-- Simulation UI -->
                <div
                    style="position: absolute; top: 20px; left: 20px; font-family: 'Courier New', monospace; color: var(--neon-cyan); font-size: 12px;">
                    > INITIALIZING NEURAL LINK...<br>
                    > CONNECTED TO CORE<br>
                    > MONITORING TRAFFIC...
                </div>

                <!-- Scanning Line -->
                <div
                    style="position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: var(--neon-cyan); box-shadow: 0 0 10px var(--neon-cyan); animation: scan 3s infinite linear;">
                </div>

                <!-- Detected Threats -->
                <div style="position: absolute; bottom: 20px; right: 20px; text-align: right;">
                    <div style="color: var(--danger); font-weight: bold; margin-bottom: 5px;">THREAT BLOCKED</div>
                    <div style="color: var(--text-muted); font-size: 12px;">CONFIDENCE: 99.8%</div>
                </div>

                <!-- Center Visual -->
                <div
                    style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 200px; height: 200px; border: 1px dashed var(--neon-purple); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                    <div
                        style="width: 180px; height: 180px; border: 1px solid var(--neon-cyan); border-radius: 50%; animation: pulse 2s infinite;">
                    </div>
                </div>
            </div>

            <div style="text-align: center; margin-top: 40px;">
                <p
                    style="color: var(--text-muted); margin-bottom: 20px; max-width: 600px; margin-left: auto; margin-right: auto;">
                    Our advanced computer vision models analyze content in milliseconds, blocking threats before they
                    reach your screen.
                    Powered by the NudeNet 640m High-Precision Model.
                </p>
                <a href="#download" class="btn btn-primary">DEPLOY PROTECTION</a>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="section">
        <div class="container">
            <div class="section-header">
                <h2 class="text-gradient">DEFENSE MODULES</h2>
                <p style="color: var(--text-muted);">OPERATIONAL CAPABILITIES</p>
            </div>

            <div class="grid">
                <div class="card">
                    <div class="card-icon">🧠</div>
                    <h3>NEURAL ENGINE</h3>
                    <p>Real-time image and text analysis using ensemble ML models (CLIP, ResNet, BERT). 99.8% detection
                        accuracy with < 50ms latency.</p>
                </div>
                <div class="card">
                    <div class="card-icon">🔐</div>
                    <h3>QUANTUM ENCRYPTION</h3>
                    <p>All data is secured with AES-256 encryption. Zero-knowledge architecture ensures your privacy
                        remains absolute.</p>
                </div>
                <div class="card">
                    <div class="card-icon">👁️</div>
                    <h3>FORENSIC ANALYSIS</h3>
                    <p>Deep behavioral tracking generates detailed PDF reports on threat patterns, escalation risks, and
                        intervention strategies.</p>
                </div>
                <div class="card">
                    <div class="card-icon">⚡</div>
                    <h3>REAL-TIME SYNC</h3>
                    <p>Instant synchronization across all linked devices. Monitor threats from your command dashboard in
                        real-time.</p>
                </div>
                <div class="card">
                    <div class="card-icon">🛡️</div>
                    <h3>GUARDIAN LOCK</h3>
                    <p>Remote device lockdown capability for critical threat levels. Take immediate control when risks
                        escalate.</p>
                </div>
                <div class="card">
                    <div class="card-icon">📡</div>
                    <h3>SMART ALERTS</h3>
                    <p style="color: var(--text-muted);">SELECT YOUR PROTECTION LEVEL</p>
                </div>

                <div class="pricing-toggle">
                    <span class="toggle-label active" id="monthly-label">MONTHLY</span>
                    <label class="switch">
                        <input type="checkbox" id="pricing-switch">
                        <span class="slider"></span>
                    </label>
                    <span class="toggle-label" id="lifetime-label">LIFETIME</span>
                </div>

                <div class="grid" style="max-width: 900px; margin: 0 auto; grid-template-columns: 1fr 1fr;">
                    <!-- Monthly Plan -->
                    <div class="pricing-card" id="card-monthly">
                        <div style="color: var(--success); font-weight: 700; letter-spacing: 2px; margin-bottom: 10px;">
                            CADET ACCESS</div>
                        <h3>MONTHLY SUBSCRIPTION</h3>
                        <div class="price-amount">
                            <span
                                style="font-size: 32px; text-decoration: line-through; color: var(--text-muted); opacity: 0.5;">$10</span>
                            FREE
                        </div>
                        <div class="price-period">FOR 7 DAYS</div>
                        <p style="color: var(--success); margin-top: 10px;">THEN $10/MONTH</p>

                        <ul class="features-list">
                            <li>7-Day Free Trial</li>
                            <li>Full Neural Engine Access</li>
                            <li>Unlimited Devices</li>
                            <li>Basic Forensic Reports</li>
                            <li>Cancel Anytime</li>
                        </ul>

                        <a href="#" class="btn btn-primary" style="width: 100%;">START TRIAL</a>
                    </div>

                    <!-- Lifetime Plan -->
                            <li>Priority Neural Processing</li>
                            <li>Advanced Forensic Suite</li>
                            <li>Lifetime Updates</li>
                            <li>VIP Support Channel</li>
                        </ul>

                        <a href="#" class="btn"
                            style="width: 100%; border-color: var(--neon-purple); color: var(--neon-purple);">GET
                            LIFETIME</a>
                    </div>
                </div>
            </div>
    </section>

    <!-- Footer -->
    <footer>
        <div class="container">
            <div class="footer-grid">
                <div class="footer-col">
                    <a href="#" class="logo" style="margin-bottom: 20px;"><span>🛡️</span> ANTI-LUST GUARDIAN</a>
                    <p style="color: var(--text-muted);">Advanced AI protection for the modern digital frontier.
                        Securing the future, one byte at a time.</p>
                </div>
                <div class="footer-col">
                    <h4>MODULES</h4>
                    <ul>
                        <li><a href="#">Neural Engine</a></li>
                        <li><a href="#">Forensics</a></li>
                        <li><a href="#">Guardian Lock</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>LEGAL</h4>
                    <ul>
                        <li><a href="#">Privacy Protocol</a></li>
                        <li><a href="#">Terms of Engagement</a></li>
                        <li><a href="#">SLA</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>CONTACT</h4>
                    <ul>
                        <li><a href="#">Support Channel</a></li>
                        <li><a href="#">Report Threat</a></li>
                        <li><a href="#">System Status</a></li>
                    </ul>
                </div>
            </div>
            <div class="copyright">
                © 2025 ANTI-LUST GUARDIAN // SYSTEM VERSION 4.2.0 // ALL RIGHTS RESERVED
            </div>
        </div>
    </footer>

    <script>
        // --- Starfield Animation ---
        const canvas = document.getElementById('starfield');
        const ctx = canvas.getContext('2d');

        let width, height;
        let stars = [];

        function resize() {
            width = window.innerWidth;
            height = window.innerHeight;
            canvas.width = width;
            canvas.height = height;
            initStars();
        }

        function initStars() {
            stars = [];
            for (let i = 0; i < 200; i++) {
                stars.push({
                    x: Math.random() * width,
                    y: Math.random() * height,
                    z: Math.random() * 2 + 0.5, // Depth
                    size: Math.random() * 2,
                    speed: Math.random() * 0.5 + 0.1
                });
            }
        }

        function animateStars() {
            ctx.fillStyle = '#030014';
            ctx.fillRect(0, 0, width, height);

            stars.forEach(star => {
                // Move star
                star.y += star.speed * star.z;

                // Reset if out of bounds
                if (star.y > height) {
                    star.y = 0;
                    star.x = Math.random() * width;
                }

                // Draw star
                const brightness = Math.min(1, star.z / 2);
                ctx.fillStyle = `rgba(255, 255, 255, ${brightness})`;
                ctx.beginPath();
                ctx.arc(star.x, star.y, star.size * (star.z / 2), 0, Math.PI * 2);
                ctx.fill();

                // Draw connection lines for nearby stars (Neural effect)
                stars.forEach(otherStar => {
                    const dx = star.x - otherStar.x;
                    const dy = star.y - otherStar.y;
                    const dist = Math.sqrt(dx * dx + dy * dy);

                    if (dist < 100 && star.z > 1.5 && otherStar.z > 1.5) {
                        ctx.strokeStyle = `rgba(0, 243, 255, ${0.1 * (1 - dist / 100)})`;
                        ctx.lineWidth = 0.5;
                        ctx.beginPath();
                        ctx.moveTo(star.x, star.y);
                        ctx.lineTo(otherStar.x, otherStar.y);
                        ctx.stroke();
                    }
                });
            });

            requestAnimationFrame(animateStars);
        }

        window.addEventListener('resize', resize);
        resize();
        animateStars();

        // --- Custom Cursor ---
        const cursor = document.getElementById('cursor');
        const cursorDot = document.getElementById('cursor-dot');
        
        // Activate custom cursor only if JS runs
        document.body.classList.add('custom-cursor-active');

        document.addEventListener('mousemove', (e) => {
            cursor.style.left = e.clientX + 'px';
            cursor.style.top = e.clientY + 'px';
            cursorDot.style.left = e.clientX + 'px';
            cursorDot.style.top = e.clientY + 'px';
        });

        document.querySelectorAll('a, button, .card, .pricing-card').forEach(el => {
            el.addEventListener('mouseenter', () => cursor.classList.add('hovered'));
            el.addEventListener('mouseleave', () => cursor.classList.remove('hovered'));
        });

        // --- Header Scroll Effect ---
        const header = document.getElementById('header');
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });

        // --- Pricing Toggle ---
        const toggle = document.getElementById('pricing-switch');
        const monthlyLabel = document.getElementById('monthly-label');
        const lifetimeLabel = document.getElementById('lifetime-label');
        const cardMonthly = document.getElementById('card-monthly');
        const cardLifetime = document.getElementById('card-lifetime');

        toggle.addEventListener('change', () => {
            if (toggle.checked) {
                // Lifetime active
                monthlyLabel.classList.remove('active');
                lifetimeLabel.classList.add('active');
                cardMonthly.style.opacity = '0.5';
                cardMonthly.style.transform = 'scale(0.95)';
                cardLifetime.style.opacity = '1';
                cardLifetime.style.transform = 'scale(1.05)';
                cardLifetime.classList.add('featured');
                cardMonthly.classList.remove('featured');
            } else {
                // Monthly active
                lifetimeLabel.classList.remove('active');
                monthlyLabel.classList.add('active');
                cardLifetime.style.opacity = '0.5';
                cardLifetime.style.transform = 'scale(0.95)';
                cardMonthly.style.opacity = '1';
                cardMonthly.style.transform = 'scale(1.05)';
                cardMonthly.classList.add('featured');
                cardLifetime.classList.remove('featured');
            }
        });

        // Initialize toggle state
        cardMonthly.classList.add('featured');
        cardLifetime.style.opacity = '0.5';
        cardLifetime.style.transform = 'scale(0.95)';

    </script>
</body>

</html>
"""

with open(file_path, "w", encoding="utf-8") as f:
    f.write(full_content)

print("File reconstructed successfully.")
