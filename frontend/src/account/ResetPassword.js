import { useState } from 'react'
import FormErrors from '../components/FormErrors'
import { getPasswordReset, resetPassword } from '../lib/allauth'
import { Navigate, Link, useLocation, useLoaderData } from 'react-router-dom'
import Button from '../components/Button'

export async function resetPasswordByLinkLoader ({ params }) {
  const key = params.key
  const resp = await getPasswordReset(key)
  return { resetKey: key, resetKeyResponse: resp }
}

function ResetPassword ({ resetKey, resetKeyResponse }) {
  const [password1, setPassword1] = useState('')
  const [password2, setPassword2] = useState('')
  const [password2Errors, setPassword2Errors] = useState([])

  const [response, setResponse] = useState({ fetching: false, content: null })

  function submit () {
    if (password2 !== password1) {
      setPassword2Errors([{ param: 'password2', message: 'Password does not match.' }])
      return
    }
    setPassword2Errors([])
    setResponse({ ...response, fetching: true })
    resetPassword({ key: resetKey, password: password1 }).then((resp) => {
      setResponse((r) => { return { ...r, content: resp } })
    }).catch((e) => {
      console.error(e)
      window.alert(e)
    }).then(() => {
      setResponse((r) => { return { ...r, fetching: false } })
    })
  }
  if ([200, 401].includes(response.content?.status)) {
    return <Navigate to='/account/login' />
  }
  let body
  if (resetKeyResponse.status !== 200) {
    body = <FormErrors param='key' errors={resetKeyResponse.errors} />
  } else if (response.content?.errors?.filter(e => e.param === 'key')) {
    body = <FormErrors param='key' errors={response.content?.errors} />
  } else {
    body = (
      <>
        <div><label>Password: <input autoComplete='new-password' value={password1} onChange={(e) => setPassword1(e.target.value)} type='password' required /></label>
          <FormErrors param='password' errors={response.content?.errors} />
        </div>
        <div><label>Password (again): <input value={password2} onChange={(e) => setPassword2(e.target.value)} type='password' required /></label>
          <FormErrors param='password2' errors={password2Errors} />
        </div>

        <Button disabled={response.fetching} onClick={() => submit()}>Reset</Button>
      </>
    )
  }

  return (
    <div>
      <h1>Reset Password</h1>
      <p>
        Remember your password? <Link to='/account/login'>Back to login.</Link>
      </p>
      {body}
    </div>
  )
}

export function ResetPasswordByLink () {
  const { resetKey, resetKeyResponse } = useLoaderData()
  return <ResetPassword resetKey={resetKey} resetKeyResponse={resetKeyResponse} />
}

export function ResetPasswordByCode () {
  const { state } = useLocation()
  if (!state || !state.resetKey || !state.resetKeyResponse) {
    return <Navigate to='/account/password/reset' />
  }
  return <ResetPassword resetKey={state.resetKey} resetKeyResponse={state.resetKeyResponse} />
}
