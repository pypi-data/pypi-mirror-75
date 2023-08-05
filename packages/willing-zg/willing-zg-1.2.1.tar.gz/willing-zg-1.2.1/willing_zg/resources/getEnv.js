import axios from 'axios';

const getEnv = (keys, url = '/api/zygoat/env/') => {
  const resolves = {};
  const rejects = {};

  const env = {};

  for (const key of keys) {
    env[key] = new Promise((resolve, reject) => {
      resolves[key] = resolve;
      rejects[key] = reject;
    })
  }

  const isSsr = typeof window === 'undefined';
  if (!isSsr) {
    axios({method: 'GET', url}).then(response => {
      for (const [key, resolve] of Object.entries(resolves)) {
        resolve(response.data[key]);
      }
    }).catch(() => {
      for (const reject of Object.values(rejects)) {
        reject();
      }
    });
  }

  env.success = keys.length
    ? Object.values(env)[0].then(() => true).catch(() => false)
    : new Promise(resolve => resolve(true));

  return env
};

export default getEnv;
