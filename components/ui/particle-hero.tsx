"use client";

import { useEffect, useRef, useState, useCallback } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

export interface ParticleHeroProps {
  name?: string;
  title?: string;
  tagline?: string;
  imageSrc?: string;
  services?: string[];
}

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  opacity: number;
}

// ─── Defaults ─────────────────────────────────────────────────────────────────

const DEFAULT_SERVICES = [
  "AI Automation",
  "AI Counselling",
  "Agentic AI",
  "AI Integration",
  "Custom Chatbot Building",
];

// ─── Component ────────────────────────────────────────────────────────────────

export function ParticleHero({
  name = "[Your Name]",
  title = "Founder & CEO — Nava AI",
  tagline = "Building the future with Artificial Intelligence",
  imageSrc = "/founder.jpg",
  services = DEFAULT_SERVICES,
}: ParticleHeroProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animFrameRef = useRef<number>(0);
  const particlesRef = useRef<Particle[]>([]);
  const goldModeRef = useRef(false);

  const [goldMode, setGoldMode] = useState(false);
  const [canvasReady, setCanvasReady] = useState(false);

  // Keep ref in sync without restarting the animation loop
  useEffect(() => {
    goldModeRef.current = goldMode;
  }, [goldMode]);

  // ── Particle initialiser ──────────────────────────────────────────────────
  const initParticles = useCallback((width: number, height: number) => {
    const count = Math.max(60, Math.floor((width * height) / 9000));
    particlesRef.current = Array.from({ length: count }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.45,
      vy: (Math.random() - 0.5) * 0.45,
      radius: Math.random() * 1.6 + 0.4,
      opacity: Math.random() * 0.55 + 0.15,
    }));
  }, []);

  // ── Canvas animation loop ─────────────────────────────────────────────────
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      initParticles(canvas.width, canvas.height);
    };

    resize();
    window.addEventListener("resize", resize);

    // Small delay so the fade-in transition fires after mount
    const readyTimer = setTimeout(() => setCanvasReady(true), 50);

    const draw = () => {
      const { width, height } = canvas;
      const gold = goldModeRef.current;
      const rgb = gold ? "212,160,23" : "100,180,255";

      ctx.clearRect(0, 0, width, height);

      const particles = particlesRef.current;
      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];

        // Move
        p.x += p.vx;
        p.y += p.vy;

        // Wrap around edges
        if (p.x < 0) p.x = width;
        else if (p.x > width) p.x = 0;
        if (p.y < 0) p.y = height;
        else if (p.y > height) p.y = 0;

        // Draw dot
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${rgb},${p.opacity})`;
        ctx.fill();

        // Draw connections (only to particles ahead to avoid double-drawing)
        for (let j = i + 1; j < particles.length; j++) {
          const q = particles[j];
          const dx = p.x - q.x;
          const dy = p.y - q.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 130) {
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(q.x, q.y);
            ctx.strokeStyle = `rgba(${rgb},${(1 - dist / 130) * 0.14})`;
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        }
      }

      animFrameRef.current = requestAnimationFrame(draw);
    };

    draw();

    return () => {
      cancelAnimationFrame(animFrameRef.current);
      clearTimeout(readyTimer);
      window.removeEventListener("resize", resize);
    };
  }, [initParticles]);

  // ── Derived theme values ──────────────────────────────────────────────────
  const accent = goldMode ? "#d4a017" : "#9dc3f7";
  const glowHex = goldMode ? "#d4a01766" : "#9dc3f766";
  const pillBg = goldMode ? "rgba(212,160,23,0.13)" : "rgba(152,192,239,0.18)";
  const pillBorder = goldMode ? "rgba(212,160,23,0.35)" : "rgba(152,192,239,0.35)";
  const beamColor = goldMode
    ? "rgba(212,160,23,VAR)"
    : "rgba(100,160,255,VAR)";
  const makBeam = (a: number) => beamColor.replace("VAR", String(a));

  // ── Stagger helper: CSS animation string with fill-forward ────────────────
  const stagger = (delay: number, duration = 0.75) =>
    `fadeSlideUp ${duration}s cubic-bezier(0.22,1,0.36,1) ${delay}s both`;

  return (
    <section
      style={{
        position: "relative",
        width: "100%",
        minHeight: "100vh",
        background: "#05060f",
        overflow: "hidden",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      {/* ── Particle canvas ─────────────────────────────────────────────── */}
      <canvas
        ref={canvasRef}
        style={{
          position: "absolute",
          inset: 0,
          width: "100%",
          height: "100%",
          opacity: canvasReady ? 1 : 0,
          transition: "opacity 1.2s ease",
        }}
      />

      {/* ── Spotlight beams ─────────────────────────────────────────────── */}
      <div
        aria-hidden
        style={{
          position: "absolute",
          inset: 0,
          pointerEvents: "none",
          opacity: canvasReady ? 1 : 0,
          transition: "opacity 2s ease 0.3s",
        }}
      >
        {/* Left beam */}
        <div
          style={{
            position: "absolute",
            top: "-15%",
            left: "18%",
            width: "3px",
            height: "130%",
            background: `linear-gradient(to bottom, ${makBeam(0.55)}, transparent)`,
            transform: "rotate(-16deg)",
            transformOrigin: "top center",
            filter: "blur(5px)",
            animation: "beamSway1 9s ease-in-out infinite",
          }}
        />
        {/* Right beam */}
        <div
          style={{
            position: "absolute",
            top: "-15%",
            right: "18%",
            width: "3px",
            height: "130%",
            background: `linear-gradient(to bottom, ${makBeam(0.5)}, transparent)`,
            transform: "rotate(16deg)",
            transformOrigin: "top center",
            filter: "blur(5px)",
            animation: "beamSway2 11s ease-in-out infinite",
          }}
        />
        {/* Center beam — thinner */}
        <div
          style={{
            position: "absolute",
            top: "-15%",
            left: "50%",
            width: "1.5px",
            height: "115%",
            background: `linear-gradient(to bottom, ${makBeam(0.35)}, transparent)`,
            transformOrigin: "top center",
            filter: "blur(3px)",
            animation: "beamSway3 13s ease-in-out infinite",
          }}
        />
      </div>

      {/* ── Ambient background glow ─────────────────────────────────────── */}
      <div
        aria-hidden
        style={{
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          width: "min(650px, 90vw)",
          height: "min(650px, 90vw)",
          borderRadius: "50%",
          background: goldMode
            ? "radial-gradient(circle, rgba(212,160,23,0.07) 0%, transparent 70%)"
            : "radial-gradient(circle, rgba(100,160,255,0.07) 0%, transparent 70%)",
          pointerEvents: "none",
        }}
      />

      {/* ── Main content ────────────────────────────────────────────────── */}
      <div
        style={{
          position: "relative",
          zIndex: 10,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          textAlign: "center",
          padding: "3rem 1.5rem 2rem",
          maxWidth: "860px",
          width: "100%",
        }}
      >
        {/* Profile photo */}
        <div
          style={{
            position: "relative",
            marginBottom: "1.75rem",
            opacity: canvasReady ? 1 : 0,
            transform: canvasReady ? "scale(1)" : "scale(0.65)",
            transition:
              "opacity 0.9s ease 0.6s, transform 0.9s cubic-bezier(0.34,1.56,0.64,1) 0.6s",
          }}
        >
          {/* Outer pulse ring */}
          <div
            aria-hidden
            style={{
              position: "absolute",
              inset: "-14px",
              borderRadius: "50%",
              border: `1.5px solid ${goldMode ? "rgba(212,160,23,0.45)" : "rgba(100,180,255,0.45)"}`,
              animation: "pulseRing 3.2s ease-in-out infinite",
            }}
          />
          {/* Inner pulse ring */}
          <div
            aria-hidden
            style={{
              position: "absolute",
              inset: "-7px",
              borderRadius: "50%",
              border: `1px solid ${goldMode ? "rgba(212,160,23,0.28)" : "rgba(100,180,255,0.28)"}`,
              animation: "pulseRing 3.2s ease-in-out infinite 0.5s",
            }}
          />
          {/* Soft halo glow */}
          <div
            aria-hidden
            style={{
              position: "absolute",
              inset: "-24px",
              borderRadius: "50%",
              background: goldMode
                ? "radial-gradient(circle, rgba(212,160,23,0.22) 0%, transparent 68%)"
                : "radial-gradient(circle, rgba(100,180,255,0.22) 0%, transparent 68%)",
              filter: "blur(10px)",
            }}
          />
          {/* Photo */}
          <img
            src={imageSrc}
            alt={`Photo of ${name}`}
            style={{
              width: "clamp(110px, 18vw, 168px)",
              height: "clamp(110px, 18vw, 168px)",
              borderRadius: "50%",
              objectFit: "cover",
              border: `2.5px solid ${goldMode ? "rgba(212,160,23,0.65)" : "rgba(100,180,255,0.65)"}`,
              display: "block",
              position: "relative",
              zIndex: 1,
            }}
          />
        </div>

        {/* Name — animated gradient heading */}
        <h1
          style={{
            fontSize: "clamp(2.4rem, 7.5vw, 5rem)",
            fontWeight: 800,
            letterSpacing: "-0.025em",
            lineHeight: 1.08,
            margin: "0 0 0.6rem",
            background: goldMode
              ? "linear-gradient(135deg, #f5d060 0%, #c8880a 35%, #f0c040 65%, #a87000 100%)"
              : "linear-gradient(135deg, #ffffff 0%, #9dc3f7 40%, #ffffff 65%, #5a9fd4 100%)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
            backgroundClip: "text",
            backgroundSize: "200% 200%",
            animation: `gradientShift 7s ease infinite, ${stagger(1, 0.8)}`,
          }}
        >
          {name}
        </h1>

        {/* Title */}
        <p
          style={{
            fontSize: "clamp(0.95rem, 2.4vw, 1.3rem)",
            fontWeight: 500,
            color: accent,
            margin: "0 0 0.65rem",
            letterSpacing: "0.05em",
            textShadow: `0 0 22px ${glowHex}`,
            animation: stagger(1.4),
          }}
        >
          {title}
        </p>

        {/* Tagline */}
        <p
          style={{
            fontSize: "clamp(0.88rem, 1.9vw, 1.1rem)",
            color: "rgba(175,200,235,0.7)",
            margin: "0 0 2.5rem",
            fontWeight: 300,
            letterSpacing: "0.025em",
            maxWidth: "520px",
            animation: stagger(1.8),
          }}
        >
          {tagline}
        </p>

        {/* Service pills */}
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            gap: "0.6rem",
            justifyContent: "center",
            maxWidth: "680px",
            width: "100%",
          }}
        >
          {services.map((service, i) => (
            <ServicePill
              key={service}
              label={service}
              delay={2 + i * 0.12}
              bg={pillBg}
              border={pillBorder}
              color={accent}
              glow={glowHex}
            />
          ))}
        </div>

        {/* Gold-mode Easter-egg toggle */}
        <button
          onClick={() => setGoldMode((g) => !g)}
          title={goldMode ? "Back to default" : "✨"}
          aria-label="Toggle gold mode Easter egg"
          style={{
            marginTop: "2.8rem",
            width: "11px",
            height: "11px",
            padding: 0,
            borderRadius: "50%",
            background: goldMode
              ? "#d4a017"
              : "rgba(255,255,255,0.1)",
            border: "none",
            cursor: "pointer",
            transition: "background 0.4s ease, box-shadow 0.4s ease",
            boxShadow: goldMode ? "0 0 14px #d4a017" : "none",
          }}
        />
      </div>

      {/* ── Keyframe definitions ─────────────────────────────────────────── */}
      <style>{`
        @keyframes gradientShift {
          0%,100% { background-position: 0% 50%; }
          50%      { background-position: 100% 50%; }
        }
        @keyframes fadeSlideUp {
          from { opacity: 0; transform: translateY(22px); }
          to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes pulseRing {
          0%,100% { transform: scale(1);    opacity: 0.65; }
          50%     { transform: scale(1.07); opacity: 0.18; }
        }
        @keyframes beamSway1 {
          0%,100% { transform: rotate(-16deg); opacity: 0.7; }
          50%     { transform: rotate(-10deg); opacity: 0.38; }
        }
        @keyframes beamSway2 {
          0%,100% { transform: rotate(16deg); opacity: 0.45; }
          50%     { transform: rotate(22deg); opacity: 0.75; }
        }
        @keyframes beamSway3 {
          0%,100% { transform: translateX(-50%) rotate(-4deg); opacity: 0.28; }
          50%     { transform: translateX(-50%) rotate(4deg);  opacity: 0.58; }
        }

        /* Mobile: cap pills to ~2 per row */
        @media (max-width: 480px) {
          .ph-pills { gap: 0.5rem !important; }
          .ph-pill  { font-size: 0.78rem !important; padding: 0.38rem 0.9rem !important; }
        }
      `}</style>
    </section>
  );
}

// ─── ServicePill sub-component ────────────────────────────────────────────────

interface PillProps {
  label: string;
  delay: number;
  bg: string;
  border: string;
  color: string;
  glow: string;
}

function ServicePill({ label, delay, bg, border, color, glow }: PillProps) {
  const [hovered, setHovered] = useState(false);

  return (
    <span
      className="ph-pill"
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        display: "inline-block",
        padding: "0.42rem 1.05rem",
        borderRadius: "999px",
        background: bg,
        border: `1px solid ${hovered ? color : border}`,
        color,
        fontSize: "clamp(0.78rem, 1.4vw, 0.9rem)",
        fontWeight: 500,
        letterSpacing: "0.03em",
        cursor: "default",
        userSelect: "none",
        animation: `fadeSlideUp 0.6s cubic-bezier(0.22,1,0.36,1) ${delay}s both`,
        boxShadow: hovered
          ? `0 0 20px ${glow}, 0 0 7px ${glow}`
          : "none",
        transition: "box-shadow 0.28s ease, border-color 0.28s ease",
      }}
    >
      {label}
    </span>
  );
}
