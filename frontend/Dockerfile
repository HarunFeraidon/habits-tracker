FROM node:18

WORKDIR /code/frontend

COPY . /code/frontend

# Install dependencies
RUN npm install

# Expose port 3000 for React
EXPOSE 3000

# Start the React application
CMD ["npm", "start"]