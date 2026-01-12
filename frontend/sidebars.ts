import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  // But you can create a sidebar manually
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Getting Started',
      collapsed: false,
      items: [
        'intro',
      ],
    },
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      collapsible: true,
      collapsed: false,
      items: [
        'module-1/chapter-1-introduction',
        'module-1/chapter-2-communication-primitives',
        'module-1/chapter-3-ai-robot-bridge',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      collapsible: true,
      collapsed: false,
      items: [
        'module-2-digital-twin/intro',
        'module-2-digital-twin/gazebo-physics',
        'module-2-digital-twin/sensors-simulation',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
      collapsible: true,
      collapsed: false,
      items: [
        'module-3-ai-brain/perception-training',
        'module-3-ai-brain/spatial-intelligence',
        'module-3-ai-brain/navigation-planning',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA) & The Autonomous Humanoid',
      collapsible: true,
      collapsed: false,
      items: [
        'module-4-vla-autonomous/vla-systems',
        'module-4-vla-autonomous/voice-to-action',
        'module-4-vla-autonomous/capstone-autonomous',
      ],
    },
  ],
};

export default sidebars;
