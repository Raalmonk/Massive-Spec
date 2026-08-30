/** Shared Tailwind config for the M-Spec pages (timeline + main menu).
 *  Replaces the cdn.tailwindcss.com runtime; theme extension mirrors the
 *  former inline `tailwind.config` block in main_menu.html. */
module.exports = {
  darkMode: "class",
  content: [
    "./timeline.html",
    "./main_menu.html",
    "./src/**/*.jsx",
  ],
  theme: {
    extend: {
      fontFamily: {
        // Inter 走自托管 (见 src/tailwind.css), 后面接各平台的系统中日韩字体,
        // 因为 Inter 的 latin 子集不含 CJK, 站点却有中/日/韩 三种界面语言
        sans: [
          "Inter",
          "system-ui",
          "-apple-system",
          "Segoe UI",
          "PingFang SC",
          "Hiragino Sans",
          "Yu Gothic UI",
          "Microsoft YaHei",
          "Malgun Gothic",
          "Noto Sans CJK SC",
          "sans-serif",
        ],
        mono: ["ui-monospace", "SFMono-Regular", "Menlo", "Consolas", "monospace"],
      },
      colors: {
        gray: {
          850: "#1f2937",
          900: "#111827",
          950: "#030712",
        },
        // Main Theme Color (Monk Green)
        monk: {
          DEFAULT: "#00FF96",
          dim: "#00cc78",
          dark: "#009e5f",
        },
        // Custom FF14 Job Colors
        job: {
          pld: "#A8D2E6", war: "#CF2621", drk: "#D126CC", gnb: "#796D30",
          whm: "#FFF0F5", sch: "#8657FF", ast: "#FFE74A", sge: "#80A0F0",
          mnk: "#D69C00", drg: "#4164CD", nin: "#AF1964", sam: "#E46D04", rpr: "#965A90", vpr: "#108221",
          brd: "#91BA5E", mch: "#6EE1D6", dnc: "#E2B0AF",
          blm: "#A579D6", smn: "#2D9B78", rdm: "#E87B7B", pct: "#FF66CC",
        },
      },
    },
  },
};
