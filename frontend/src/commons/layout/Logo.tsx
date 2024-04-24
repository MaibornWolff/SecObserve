import { getSettingTheme } from "../user_settings/functions";

const Logo = () => {
    if (getSettingTheme() == "dark") {
        return <img src="secobserve_white.svg" height={"20px"} />;
    } else {
        return <img src="secobserve.svg" height={"20px"} />;
    }
};

export default Logo;
