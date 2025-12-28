import type {ReactNode} from 'react';
import clsx from 'clsx';
import styles from './callouts.module.css';

type EquationBoxProps = {
  children: ReactNode;
  label?: string;
};

export default function EquationBox({children, label}: EquationBoxProps): ReactNode {
  return (
    <div className={clsx('equation-box', styles.equationBox)}>
      <div className={styles.equationContent}>{children}</div>
      {label && <div className={styles.equationLabel}>{label}</div>}
    </div>
  );
}