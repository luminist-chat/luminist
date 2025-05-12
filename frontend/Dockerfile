# Stage 1: Build the React frontend
FROM node:20-alpine AS build

WORKDIR /app

# Install dependencies first (cache-friendly)
COPY package.json package-lock.json ./
RUN npm install

# Copy remaining files
COPY . .

# Build the app
RUN npm run build

# Stage 2: Serve the built files with a lightweight server
FROM nginx:stable-alpine

# Copy built files from previous stage
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Run Nginx
CMD ["nginx", "-g", "daemon off;"]
