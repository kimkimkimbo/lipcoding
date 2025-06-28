import styled from 'styled-components';
import Link from 'next/link';
import { ReactNode } from 'react';

const Wrapper = styled.div`
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: ${({ theme }) => theme.colors.background};
`;

const Header = styled.header`
  width: 100%;
  background: ${({ theme }) => theme.colors.primary};
  color: #fff;
  padding: 1.2em 0;
  text-align: center;
  font-size: 1.4rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  box-shadow: 0 2px 8px rgba(179,157,219,0.08);
`;

const Nav = styled.nav`
  display: flex;
  justify-content: center;
  gap: 2em;
  margin: 1em 0;
`;

const Main = styled.main`
  flex: 1;
  width: 100%;
  max-width: 700px;
  margin: 0 auto;
  padding: 2em 1em 3em 1em;
`;

const Footer = styled.footer`
  width: 100%;
  background: ${({ theme }) => theme.colors.primaryLight};
  color: ${({ theme }) => theme.colors.textSecondary};
  text-align: center;
  padding: 1em 0;
  font-size: 0.95rem;
`;

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <Wrapper>
      <Header>멘토-멘티 매칭</Header>
      <Nav>
        <Link href="/mentors">멘토 찾기</Link>
        <Link href="/profile">내 프로필</Link>
        <Link href="/match">매칭 요청</Link>
        <Link href="/login">로그인</Link>
      </Nav>
      <Main>{children}</Main>
      <Footer>© 2025 Mentor-Mentee App</Footer>
    </Wrapper>
  );
}
