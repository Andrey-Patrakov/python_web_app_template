FROM node:lts-alpine as build-stage

ARG BACKEND_URL
RUN echo $env:BACKEND_URL
ENV VITE_API_ROOT=$BACKEND_URL

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build


FROM nginx:stable-alpine as production-stage
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]