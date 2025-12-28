import type {ReactNode} from 'react';
import clsx from 'clsx';
import styles from './callouts.module.css';

type DefinitionBoxProps = {
  children: ReactNode;
  title?: string;
};

export default function DefinitionBox({children, title = 'DEFINITION'}: DefinitionBoxProps): ReactNode {
  return (
    <div className={clsx('definition-box', styles.definitionBox)}>
      <div className={styles.definitionTitle}>{title}</div>
      <div className={styles.definitionContent}>{children}</div>
    </div>
  );
}