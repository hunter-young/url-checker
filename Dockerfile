FROM node:lts-alpine as build
COPY . . 
WORKDIR /ui/url-checker

RUN npm install && npm run build
RUN npm prune --production

FROM python:3.9.5-alpine
COPY --from=build . .

RUN apk add --no-cache --virtual .build-deps gcc g++ musl-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]