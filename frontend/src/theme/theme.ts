import { palette } from './palette';

export const theme = {
  colors: palette,
  borderRadius: '12px',
  boxShadow: '0 2px 8px rgba(179,157,219,0.08)',
  fontFamily: 'Pretendard, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif',
  transition: 'all 0.2s cubic-bezier(.4,0,.2,1)',
};

export type ThemeType = typeof theme;
