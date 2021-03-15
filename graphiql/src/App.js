import logo from './logo.svg';
import './App.css';

import GraphiQL from 'graphiql';
import 'graphiql/graphiql.min.css';

const App = () => (
  <GraphiQL
    fetcher={async graphQLParams => {
      const data = await fetch(
        'http://localhost:8080/graphql',
        {
          method: 'POST',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(graphQLParams),
          credentials: 'same-origin',
        },
      );
      return data.json().catch(() => data.text());
    }}
  />
);
export default App;
