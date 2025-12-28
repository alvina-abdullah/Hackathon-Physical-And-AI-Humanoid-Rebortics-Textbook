import type {ReactNode} from 'react';
import clsx from 'clsx';
import styles from './callouts.module.css';

type KeyIdeaBoxProps = {
  children: ReactNode;
  title?: string;
};

export default function KeyIdeaBox({children, title = 'KEY IDEA'}: KeyIdeaBoxProps): ReactNode {
  return (
    <div className={clsx('key-idea-box', styles.keyIdeaBox)}>
      <div className={styles.keyIdeaTitle}>{title}</div>
      <div className={styles.keyIdeaContent}>{children}</div>
    </div>
  );
}