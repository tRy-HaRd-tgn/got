# ���������� ����������� ����� Node.js ��� ������ ����������
FROM node:22 as build

# ������������� ������� ����������
WORKDIR /app

# �������� package.json � package-lock.json
COPY package*.json ./

# ������������� �����������
RUN npm install

# �������� �������� ���
COPY . .

# �������� ����������
RUN npm run build

# ���������� ����������� ����� Nginx ��� ����������
FROM nginx:alpine

# �������� ��������� ����� �� ����������� ����� � ����� Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# �������� ������������ Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# ��������� ���� 80
EXPOSE 80

# ��������� Nginx
CMD ["nginx", "-g", "daemon off;"]