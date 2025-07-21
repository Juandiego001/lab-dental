# Prepare nuxt
FROM node:22-alpine AS builder

WORKDIR /app
COPY . .
RUN npm install && npm run build

# Real production server
FROM node:22-alpine
COPY --from=builder /app/.output ./.output
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./

EXPOSE 3000

CMD ["node", ".output/server/index.mjs"]
