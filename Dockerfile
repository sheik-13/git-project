# Use official Nginx lightweight image
FROM nginx:alpine

# Copy your static files into nginx's default directory
COPY . /usr/share/nginx/html

# Expose port 80 for web traffic
EXPOSE 80
