import axios from 'axios';

const TOKEN_REFRESH_INTERVAL = 4 * 60 * 1000; // 4 min in ms

export const withReturn = url => {
  if (typeof window === 'undefined') {
    // server side rendering, so we don't know where to return to
    return url;
  }
  const params = new URLSearchParams();
  params.append('next', window.location.href);
  return `${url}?${params.toString()}`;
};

class TokenFetcher {
  constructor() {
    this.portunusUrl = '';
    this.fetchFunction = this.defaultFetch;
    this.onError = this.defaultOnError;
    this.onSuccess = this.defaultOnSuccess;
    this.currentToken = '';
    this.timerId = null;
    this.tokenCallbacks = [];
  }

  get loginUrl() {
    return withReturn(`${this.portunusUrl}/login`);
  }

  defaultFetch() {
    return axios({
      method: 'post',
      url: `${this.portunusUrl}/api/auth/token/refresh/`,
      withCredentials: true,
    });
  }

  defaultOnError() {
    window.location.replace(this.loginUrl);
  }

  defaultOnSuccess = () => null;

  get accessToken() {
    return new Promise(resolve => {
      if (this.currentToken) {
        resolve(this.currentToken);
      } else {
        this.tokenCallbacks.push(resolve);
      }
    });
  }

  fetchToken = async () => {
    try {
      const response = await this.fetchFunction();
      this.currentToken = response.data.access;
      this.onSuccess(this.currentToken);
      this.clearCallbacks();
      return true;
    } catch (error) {
      if (error.response) {
        if (error.response.status === 401) {
          this.clearToken();
        }
      }
      this.onError(error);
    }
    return false;
  };

  clearToken() {
    this.currentToken = '';
    clearInterval(this.timerId);
    this.timerId = null;
    this.clearCallbacks();
  }

  clearCallbacks() {
    this.tokenCallbacks.forEach(cb => cb(this.currentToken));
    this.tokenCallbacks = [];
  }

  start(portunusUrl, fetchFn, onSuccess, onError) {
    this.portunusUrl = portunusUrl || this.portunusUrl;
    this.fetchFunction = fetchFn || this.defaultFetch;
    this.onSuccess = onSuccess || this.defaultOnSuccess;
    this.onError = onError || this.defaultOnError;
    if (!this.timerId) {
      this.timerId = setInterval(this.fetchToken, TOKEN_REFRESH_INTERVAL);
      this.fetchToken();
    }
  }
}

const tokenFetcher = new TokenFetcher();

export default tokenFetcher;
