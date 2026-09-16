// next.config.js
const repo = "Notus-Next.js"; // replace with your actual repo name

module.exports = {
  output: "export",
  basePath: `/${repo}`,
  assetPrefix: `/${repo}/`,
  images: { unoptimized: true, disableStaticImages: true },
};
