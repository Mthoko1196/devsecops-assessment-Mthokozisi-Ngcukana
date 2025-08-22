# ---------- builder ----------
FROM node:20.12.2-alpine AS builder
WORKDIR /app
ENV NODE_ENV=production
# copy only manifests first to leverage layer caching
COPY application/package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci
# now copy source and build
COPY application/ ./
# If CRA/Vite uses "build" script
RUN npm run build

# ---------- runtime ----------
# NGINX as a tiny static server
FROM nginx:1.27-alpine AS runtime
# run nginx on an unprivileged port and as non-root
USER 101:101
WORKDIR /usr/share/nginx/html
# remove default content, copy build output
RUN rm -rf ./*
COPY --from=builder /app/dist ./  # Vite default
# If CRA, swap to: COPY --from=builder /app/build ./
# Harden NGINX config: listen on 8080, disable server tokens, basic security headers
COPY application/nginx.conf /etc/nginx/conf.d/default.conf

# runtime protections
# read-only rootfs is enforced via Compose/K8s (see below)
# expose unprivileged port
EXPOSE 8080
# healthcheck happens in Compose/K8s; keep entrypoint default