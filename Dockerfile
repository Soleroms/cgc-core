FROM node:18 
WORKDIR /app 
COPY . . 
RUN npm install 
RUN chmod +x node_modules/.bin/vite 
RUN npm run build 
CMD ["npm", "run", "start"]
