# SafeAlert Dispatch Web Application

A modern web application for managing emergency alerts, teams, and responders in real-time.

## Features

- Real-time alert monitoring and management
- Team and responder coordination
- User management and role-based access control
- Interactive map visualization
- Report generation and analytics
- WebSocket-based real-time updates

## Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)
- A Mapbox API token for map functionality

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/safealert.git
cd safealert/dispatch-web
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file in the root directory and add the following environment variables:
```env
REACT_APP_API_URL=http://localhost:3001/api
REACT_APP_WEBSOCKET_URL=http://localhost:3001
REACT_APP_MAPBOX_TOKEN=your_mapbox_token_here
```

## Development

To start the development server:

```bash
npm start
```

The application will be available at `http://localhost:3000`.

## Building for Production

To create a production build:

```bash
npm run build
```

The build artifacts will be stored in the `build/` directory.

## Testing

To run the test suite:

```bash
npm test
```

## Project Structure

```
dispatch-web/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/         # Page components
│   ├── services/      # API and WebSocket services
│   ├── store/         # Redux store and slices
│   ├── theme/         # Material-UI theme configuration
│   ├── types/         # TypeScript type definitions
│   ├── config/        # Application configuration
│   ├── App.tsx        # Main application component
│   └── index.tsx      # Application entry point
├── public/            # Static assets
├── package.json       # Project dependencies and scripts
├── tsconfig.json      # TypeScript configuration
└── README.md         # Project documentation
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 