import { startHttpServer } from './server';

startHttpServer().catch((err) => {
  console.error('Fatal error:', err);
  process.exit(1);
});
