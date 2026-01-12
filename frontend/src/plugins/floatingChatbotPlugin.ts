import {Plugin, LoadContext} from '@docusaurus/types';
import path from 'path';

export default function FloatingChatbotPlugin(): Plugin<undefined> {
  return {
    name: 'floating-chatbot-plugin',

    getClientModules() {
      return [path.resolve(__dirname, './components/FloatingChatbotWrapper')];
    },
  };
}