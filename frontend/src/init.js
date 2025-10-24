import { setup } from './lib/allauth'

export function init () {
  if (document.location.hostname === 'app.react.demo.allauth.org') {
    setup('app', 'https://api.react.demo.allauth.org/_allauth/app/v1', false)
  } else if (document.location.hostname === 'react.demo.allauth.org') {
    setup('browser', 'https://api.react.demo.allauth.org/_allauth/browser/v1', true)
  } else {
    // Local development setup - use full backend URL
    const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000'
    setup('browser', `${apiUrl}/api/_allauth/browser/v1`, true)
  }
}
