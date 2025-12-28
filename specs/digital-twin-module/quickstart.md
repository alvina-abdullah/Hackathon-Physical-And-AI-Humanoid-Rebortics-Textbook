# Quickstart Guide: Module-2 — The Digital Twin (Gazebo & Unity)

## Prerequisites

- Node.js (version 18.x or higher)
- npm or yarn package manager
- Git for version control
- Access to the existing Docusaurus project in the frontend directory

## Setup Instructions

### 1. Navigate to your project
```bash
cd frontend
```

### 2. Verify the module-2-digital-twin directory exists
```bash
mkdir -p docs/module-2-digital-twin
```

### 3. The three chapter files should already exist:
- `docs/module-2-digital-twin/intro.md`
- `docs/module-2-digital-twin/gazebo-physics.md`
- `docs/module-2-digital-twin/sensors-simulation.md`

### 4. Update sidebar configuration in `sidebars.ts` to include Module 2
```javascript
{
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'module-1/chapter-1-introduction',
        'module-1/chapter-2-communication-primitives',
        'module-1/chapter-3-ai-robot-bridge',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'module-2-digital-twin/intro',
        'module-2-digital-twin/gazebo-physics',
        'module-2-digital-twin/sensors-simulation',
      ],
    },
    {
      type: 'category',
      label: 'Tutorial',
      items: ['tutorial-basics/create-a-document'],
    },
  ],
}
```

### 5. Start the development server to verify the new module
```bash
npm start
```

## Content Creation Guidelines

### Chapter 1: Introduction to Digital Twins in Physical AI
- Focus on what digital twins are and their role in Physical AI
- Explain the importance of simulation before real-world deployment
- Provide overview of Gazebo and Unity capabilities
- Describe the simulation-to-reality pipeline

### Chapter 2: Physics Simulation in Gazebo
- Explain core physics concepts: gravity, collisions, joints
- Describe how humanoid robots move in Gazebo simulation
- Explain why accurate physics is important for AI training
- Cover simulation parameters and tuning

### Chapter 3: Sensor Simulation in Digital Twins
- Cover simulation of LiDAR, depth cameras, and IMUs
- Explain sensor data flow to AI systems
- Describe how to prepare perception pipelines for later modules

## Validation Checklist

- [ ] All chapters follow Docusaurus Markdown format
- [ ] Frontmatter includes required fields (id, title, sidebar_position)
- [ ] Content aligns with functional requirements
- [ ] Success criteria are met
- [ ] Content renders correctly in development server
- [ ] Navigation works properly in sidebar
- [ ] All links function correctly
- [ ] Concept-first approach maintained without heavy code dumps
- [ ] Examples grounded in humanoid robotics context