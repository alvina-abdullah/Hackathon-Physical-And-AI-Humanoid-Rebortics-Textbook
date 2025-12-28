import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero', styles.heroBanner)}>
      <div className="container">
        <div className="row">
          <div className="col ">
            <div className={styles.heroTextContent}>
              <Heading as="h1" className="hero__title">
                {siteConfig.title}
              </Heading>
              <p className="hero__subtitle">{siteConfig.tagline}</p>
              {/* <div className={styles.buttons}>
                <Link
                  className="button button--primary button--lg"
                  to="/docs/intro">
                  Begin Your Robotics Journey
                </Link>
                <Link
                  className="button button--secondary button--lg"
                  to="/docs/module-1/chapter-1-introduction">
                  Start with ROS 2
                </Link>
              </div> */}
            </div>
          </div>
          <div className="col col--5">
            <div className={styles.heroImageContainer}>
              <img
                src="/img/robot.png"
                alt="Humanoid Robot"
                className={styles.robotImage}
                onError={(e) => {
                  const target = e.target as HTMLImageElement;
                  target.src = "/img/robot.png";
                }}
              />
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

function HomepageModules() {
  return (
    <section className={styles.modules}>
      <div className="container padding-vert--lg">
        <div className="row">
          <div className="col col--4">
            <div className={styles.moduleCard}>
              <h3>Module 1: The Robotic Nervous System</h3>
              <p>Learn ROS 2 fundamentals, communication primitives, and how to bridge AI systems with robotic hardware.</p>
              <Link to="/docs/module-1/chapter-1-introduction" className={styles.moduleLink}>
                Explore ROS 2 →
              </Link>
            </div>
          </div>
          <div className="col col--4">
            <div className={styles.moduleCard}>
              <h3>Module 2: The Digital Twin</h3>
              <p>Master simulation environments with Gazebo and Unity for creating accurate virtual replicas of physical systems.</p>
              <Link to="/docs/module-2-digital-twin/intro" className={styles.moduleLink}>
                Explore Simulation →
              </Link>
            </div>
          </div>
          <div className="col col--4">
            <div className={styles.moduleCard}>
              <h3>Module 3: The AI-Robot Brain</h3>
              <p>Understand NVIDIA Isaac Sim & Isaac ROS for perception, spatial intelligence, and navigation planning.</p>
              <Link to="/docs/module-3-ai-brain/perception-training" className={styles.moduleLink}>
                Explore AI Brain →
              </Link>
            </div>
          </div>
        </div>
        <div className="row padding-top--lg">
          <div className="col col--4 col--offset-2">
            <div className={styles.moduleCard}>
              <h3>Module 4: Vision-Language-Action Systems</h3>
              <p>Build autonomous humanoid robots using VLA systems for voice-to-action capabilities.</p>
              <Link to="/docs/module-4-vla-autonomous/vla-systems" className={styles.moduleLink}>
                Explore VLA Systems →
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}



export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Home | ${siteConfig.title}`}
      description="Advanced Robotics Education Platform - Physical AI and Humanoid Robotics">
      <HomepageHeader />
      <main>
        <HomepageModules />
  
      </main>
    </Layout>
  );
}
