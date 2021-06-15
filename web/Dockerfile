# develop stage
FROM node:14 as develop-stage
WORKDIR /usr/app
COPY web/package*.json ./
RUN yarn global add @vue/cli \
    # && yarn global add @vue/cli-service-global \
    && yarn install
COPY web/ .

# build stage
FROM develop-stage as build-stage
RUN yarn build

# production stage
FROM nginx:1.17.10-alpine as production-stage
COPY --from=build-stage /usr/app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
