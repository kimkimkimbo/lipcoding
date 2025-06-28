import Head from 'next/head';
import styled from 'styled-components';

const HomeContainer = styled.div`
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: ${({ theme }) => theme.colors.background};
`;

const Title = styled.h1`
  color: ${({ theme }) => theme.colors.primaryDark};
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5em;
`;

const Subtitle = styled.p`
  color: ${({ theme }) => theme.colors.textSecondary};
  font-size: 1.2rem;
  margin-bottom: 2em;
`;

const MainButton = styled.a`
  display: inline-block;
  background: ${({ theme }) => theme.colors.primary};
  color: #fff;
  padding: 0.8em 2em;
  border-radius: ${({ theme }) => theme.borderRadius};
  font-size: 1.1rem;
  font-weight: 600;
  box-shadow: ${({ theme }) => theme.boxShadow};
  transition: background 0.2s;
  &:hover {
    background: ${({ theme }) => theme.colors.primaryDark};
  }
`;

export default function Home() {
  return (
    <>
      <Head>
        <title>멘토-멘티 매칭 | Mentor-Mentee App</title>
        <meta name="description" content="멘토와 멘티를 쉽고 빠르게 매칭하는 서비스" />
      </Head>
      <HomeContainer>
        <Title>멘토-멘티 매칭</Title>
        <Subtitle>파스텔 보라색의 미니멀한 UI, 쉽고 빠른 멘토링 매칭 경험을 제공합니다.</Subtitle>
        <MainButton href="/login">시작하기</MainButton>
      </HomeContainer>
    </>
  );
}
