import { Provider } from 'react-redux';
import store from '@/store/store.js'; // Your Redux store

const ReduxProvider = ({ children }) => {
    return <Provider store={store}>{children}</Provider>;
};

export default ReduxProvider;