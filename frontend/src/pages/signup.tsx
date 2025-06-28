import Head from 'next/head';
import styled from 'styled-components';
import { useForm } from 'react-hook-form';
import * as yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import axios from 'axios';
import { useState } from 'react';
import Layout from '../components/Layout';

const schema = yup.object().shape({
  email: yup.string().email('이메일 형식이 올바르지 않습니다.').required('이메일을 입력하세요.'),
  password: yup.string().min(8, '비밀번호는 8자 이상이어야 합니다.').required('비밀번호를 입력하세요.'),
  name: yup.string().min(1).max(30).required('이름을 입력하세요.'),
  role: yup.string().oneOf(['mentor', 'mentee'], '역할을 선택하세요.').required('역할을 선택하세요.'),
});

type SignupForm = {
  email: string;
  password: string;
  name: string;
  role: 'mentor' | 'mentee';
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

export default function SignupPage() {
  const { register, handleSubmit, formState: { errors } } = useForm<SignupForm>({ resolver: yupResolver(schema) });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const onSubmit = async (data: SignupForm) => {
    setError('');
    setSuccess(false);
    try {
      await axios.post('/api/signup', data);
      setSuccess(true);
      setTimeout(() => window.location.href = '/login', 1200);
    } catch (e: any) {
      setError(e.response?.data?.error || '회원가입에 실패했습니다.');
    }
  };

  return (
    <Layout>
      <Head>
        <title>회원가입 | 멘토-멘티 매칭</title>
      </Head>
      <Form onSubmit={handleSubmit(onSubmit)}>
        <h2>회원가입</h2>
        <label>
          이메일
          <Input type="email" {...register('email')} autoComplete="username" />
          {errors.email && <ErrorMsg>{errors.email.message}</ErrorMsg>}
        </label>
        <label>
          비밀번호
          <Input type="password" {...register('password')} autoComplete="new-password" />
          {errors.password && <ErrorMsg>{errors.password.message}</ErrorMsg>}
        </label>
        <label>
          이름
          <Input type="text" {...register('name')} />
          {errors.name && <ErrorMsg>{errors.name.message}</ErrorMsg>}
        </label>
        <label>
          역할
          <select {...register('role')} defaultValue="">
            <option value="" disabled>선택하세요</option>
            <option value="mentor">멘토</option>
            <option value="mentee">멘티</option>
          </select>
          {errors.role && <ErrorMsg>{errors.role.message}</ErrorMsg>}
        </label>
        {error && <ErrorMsg>{error}</ErrorMsg>}
        {success && <div style={{color:'#81c784'}}>회원가입 성공! 로그인 페이지로 이동합니다.</div>}
        <SubmitBtn type="submit">회원가입</SubmitBtn>
        <div style={{textAlign:'center',marginTop:'1em'}}>
          <a href="/login">로그인</a>
        </div>
      </Form>
    </Layout>
  );
}
