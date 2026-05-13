#!/usr/bin/env node

/**
 * Phase 6 Backend Startup Script
 * Starts the Express server with all Phase 5 security and compliance components
 */

const { spawn } = require('child_process');

console.log('🚀 Starting Phase 6 Backend Server...');
console.log('🔒 Integrating Phase 5 Security & Compliance...');
console.log('🔗 Connecting Phase 6 Frontend...');

// Start the backend server
const serverProcess = spawn('node', ['src/server.js'], {
  stdio: 'inherit',
  env: {
    ...process.env,
    ENCRYPTION_KEY: 'test_encryption_key_for_phase5_startup'
  }
});

// Handle server output
serverProcess.stdout.on('data', (data) => {
  console.log(data.toString());
});

serverProcess.stderr.on('data', (data) => {
  console.error(data.toString());
});

serverProcess.on('close', (code) => {
  if (code === 0) {
    console.log('✅ Phase 6 Backend Server started successfully');
    console.log('🌐 Ready for Phase 6 Frontend integration');
  } else {
    console.error('❌ Phase 6 Backend Server failed to start');
    console.error(`Exit code: ${code}`);
  }
});

// Start frontend development server
const frontendProcess = spawn('npm', ['run', 'preview'], {
  stdio: 'inherit',
  cwd: './frontend'
});

// Handle frontend output
frontendProcess.stdout.on('data', (data) => {
  console.log(data.toString());
});

frontendProcess.stderr.on('data', (data) => {
  console.error(data.toString());
});

frontendProcess.on('close', (code) => {
  if (code === 0) {
    console.log('✅ Phase 6 Frontend development server started');
  } else {
    console.error('❌ Phase 6 Frontend development server failed to start');
    console.error(`Exit code: ${code}`);
  }
});
