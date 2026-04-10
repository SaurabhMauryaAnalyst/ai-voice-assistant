# ─── STAGE 1: BUILD ──────────────────────────────────────
# Use Node.js 20 Alpine (small Linux) as the build environment
# "AS builder" names this stage so we can reference it later
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files FIRST — before source code
# Why? Docker caches each layer. If only source code changed
# (not package.json), this layer is cached → npm ci is skipped → fast rebuild
COPY package*.json ./
RUN npm ci --frozen-lockfile      # install exact versions from lockfile

# NOW copy source code (this layer re-runs on every code change)
COPY . .

# Accept the WebSocket URL as a build-time argument
# Vite bakes this into the compiled JS bundle at build time
ARG VITE_WS_URL
ENV VITE_WS_URL=$VITE_WS_URL

# Compile React → static HTML/CSS/JS in the /app/dist folder
RUN npm run build

# At this point Stage 1 has: node_modules (400MB), src/, dist/, etc.
# We only want: dist/


# ─── STAGE 2: RUNTIME ────────────────────────────────────
# Start completely fresh with a tiny nginx image (~23MB)
FROM nginx:1.27-alpine

# Copy ONLY the compiled output from Stage 1
# Everything else in Stage 1 is discarded — not in final image
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy our nginx config (handles SPA routing, WebSocket proxying)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

# Final image size: ~25MB  (vs ~450MB without multi-stage)