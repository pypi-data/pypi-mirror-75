import { observer } from 'mobx-react';

const setDepartment = department => {
  if (typeof window === 'undefined') {
    return;
  }

  window.zESettings = {
    webWidget: {
      chat: {
        departments: {
          enabled: [department],
        },
      },
    },
  };
};

const defaultDepartment = 'Members';
import('utils/constants/chat').then(module => {
  setDepartment(module.ZENDESK_CHAT_DEPARTMENT || defaultDepartment);
});

const ChatWidget = key => {
  const widgetUrl = `https://static.zdassets.com/ekr/snippet.js?key=${key}`;

  return <script id="ze-snippet" src={widgetUrl} async defer />;
};

export default observer(ChatWidget);
