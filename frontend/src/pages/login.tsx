import Head from 'next/head';
import styled from 'styled-components';
import { useForm } from 'react-hook-form';
import * as yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import axios from 'axios';
import { useState } from 'react';
import Layout from '../components/Layout';


const schema = yup.object({
  email: yup.string().email('유효한 이메일을 입력하세요.').required('이메일을 입력하세요.'),
  password: yup.string().required('비밀번호를 입력하세요.'),
});

type LoginForm = {
  email: string;
  password: string;
};

const Form = styled.form`
  background: ${({ theme }) => theme.colors.surface};
  border-radius: ${({ theme }) => theme.borderRadius};
  box-shadow: ${({ theme }) => theme.boxShadow};
  padding: 2em 2em 1.5em 2em;
  max-width: 400px;
  margin: 2em auto;
  display: flex;
  flex-direction: column;
  gap: 1.2em;
`;

const Input = styled.input``;
const ErrorMsg = styled.div`
  color: ${({ theme }) => theme.colors.error};
  font-size: 0.98em;
  margin-top: -0.8em;
`;
const SubmitBtn = styled.button`
  margin-top: 1em;
`;

export default function LoginPage() {
  const { register, handleSubmit, formState: { errors } } = useForm<LoginForm>({ resolver: yupResolver(schema) });
  const [error, setError] = useState('');

  const onSubmit = async (data: LoginForm) => {
    setError('');
    try {
      const res = await axios.post('/api/login', data);
      localStorage.setItem('token', res.data.token);
      window.location.href = '/profile';
    } catch (e: any) {
      setError(e.response?.data?.error || '로그인에 실패했습니다.');
    }
  };

  return (
    <Layout>
      <Head>
        <title>로그인 | 멘토-멘티 매칭</title>
      </Head>
      <Form onSubmit={handleSubmit(onSubmit)}>
        <h2>로그인</h2>
        <label>
          이메일
          <Input type="email" {...register('email')} autoComplete="username" />
          {errors.email && <ErrorMsg>{errors.email.message}</ErrorMsg>}
        </label>
        <label>
          비밀번호
          <Input type="password" {...register('password')} autoComplete="current-password" />
          {errors.password && <ErrorMsg>{errors.password.message}</ErrorMsg>}
        </label>
        {error && <ErrorMsg>{error}</ErrorMsg>}
        <SubmitBtn type="submit">로그인</SubmitBtn>
        <div style={{textAlign:'center',marginTop:'1em'}}>
          <a href="/signup">회원가입</a>
        </div>
      </Form>
    </Layout>
  );
}
