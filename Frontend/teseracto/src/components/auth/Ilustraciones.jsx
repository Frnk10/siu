const PALETAS = {
  claro: { arriba: '#ffffff', izq: '#f1f6ff', der: '#b9d4ff', y: '#1d6fe8' },
  azul: { arriba: '#4a9bf8', izq: '#1d6fe8', der: '#0b4fc0', y: '#ffffff' },
}

export const LogoTeseracto = ({ size = 64, variante = 'claro' }) => {
  const c = PALETAS[variante]
  return (
    <svg viewBox="0 0 100 100" width={size} height={size} role="img" aria-label="Teseracto">
      <polygon points="50,6 90,27 50,48 10,27" fill={c.arriba} />
      <polygon points="10,27 50,48 50,94 10,73" fill={c.izq} />
      <polygon points="90,27 50,48 50,94 90,73" fill={c.der} />
      <path
        d="M50 50 V72 M50 50 L34 41 M50 50 L66 41"
        fill="none"
        stroke={c.y}
        strokeWidth="6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

export const IlustracionLaptop = () => (
  <svg viewBox="-10 0 370 250" width="100%" style={{ maxWidth: 420 }} role="img" aria-label="Sistema protegido">
    <ellipse cx="160" cy="214" rx="165" ry="12" fill="#06339a" opacity=".25" />

    {/* Pantalla */}
    <rect x="40" y="14" width="236" height="156" rx="14" fill="#2f86f5" />
    <rect x="52" y="26" width="212" height="132" rx="6" fill="#eaf2ff" />
    <rect x="52" y="26" width="52" height="132" rx="6" fill="#4a9bf8" />
    {[46, 62, 78, 94].map((y) => (
      <rect key={y} x="62" y={y} width="32" height="5" rx="2.5" fill="#fff" opacity=".75" />
    ))}
    <rect x="116" y="38" width="136" height="108" rx="6" fill="#fff" />
    <rect x="128" y="50" width="84" height="9" rx="4.5" fill="#bcd5fb" />
    <rect x="128" y="70" width="100" height="6" rx="3" fill="#d7e5fc" />
    <rect x="128" y="84" width="76" height="6" rx="3" fill="#d7e5fc" />
    <rect x="128" y="98" width="108" height="6" rx="3" fill="#d7e5fc" />
    <rect x="128" y="112" width="64" height="6" rx="3" fill="#d7e5fc" />

    {/* Base */}
    <path d="M24 170 H292 L318 198 Q320 206 310 206 H6 Q-4 206 -2 198 Z" fill="#2a78ea" />
    <rect x="118" y="182" width="80" height="8" rx="4" fill="#1a5fd0" opacity=".6" />

    {/* Escudo con candado */}
    <g transform="translate(232 96)">
      <path
        d="M40 0 L80 14 V52 C80 82 60 100 40 110 C20 100 0 82 0 52 V14 Z"
        fill="#dcebff"
        stroke="#8fbcf9"
        strokeWidth="5"
        strokeLinejoin="round"
      />
      <path d="M40 10 L70 21 V52 C70 76 54 91 40 99 C26 91 10 76 10 52 V21 Z" fill="#3b8cf5" />
      <rect x="26" y="50" width="28" height="24" rx="5" fill="#fff" />
      <path d="M31 50 V43 a9 9 0 0 1 18 0 V50" fill="none" stroke="#fff" strokeWidth="5" strokeLinecap="round" />
      <circle cx="40" cy="60" r="3.5" fill="#3b8cf5" />
      <rect x="38.5" y="60" width="3" height="8" rx="1.5" fill="#3b8cf5" />
    </g>
  </svg>
)
