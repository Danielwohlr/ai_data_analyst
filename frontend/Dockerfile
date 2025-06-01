# Dockerfile for Next.js Frontend
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Install frontend dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the application source code
COPY . .

# Build the Next.js application (production build)
RUN npm run build

# Expose the frontend port
EXPOSE 3000

# Start the Next.js app in production mode
CMD ["npm", "start"]

