export const config = {
  baseUrl: process.env.BASE_URL ?? 'http://172.168.168.36:8006',
  accessToken: process.env.ACCESS_TOKEN ?? '',
  refreshToken: process.env.REFRESH_TOKEN ?? '',
  tenantDomain: process.env.TENANT_DOMAIN ?? '',
  secretKey: process.env.SECRET_KEY ?? '',
  port: parseInt(process.env.PORT ?? '3000', 10),
};
