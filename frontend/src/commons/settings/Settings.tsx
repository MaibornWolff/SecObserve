// import Card from "@mui/material/Card";
import { useTheme, Title } from "react-admin";
import {
    Box,
    Card,
    CardContent,
    CardHeader,
    FormControl,
    FormControlLabel,
    RadioGroup,
    Radio,
} from "@mui/material";

import { setSettingTheme, getSettingTheme } from "./functions";
import { darkTheme, lightTheme } from "../layout/themes";

const Settings = () => {
    const [, setTheme] = useTheme();

    function setLightTheme() {
        setTheme(lightTheme);
        setSettingTheme("light");
    }

    function setDarkTheme() {
        setTheme(darkTheme);
        setSettingTheme("dark");
    }

    return (
        <Card sx={{ marginTop: 2 }}>
            <Title title="Settings" />
            <CardHeader title="Settings" />
            <CardContent>
                <Box sx={{ width: "10em", display: "inline-block" }}>Theme</Box>
                <FormControl>
                    <RadioGroup
                        defaultValue={getSettingTheme()}
                        name="radio-buttons-group"
                        row
                    >
                        <FormControlLabel
                            value="light"
                            control={<Radio />}
                            label="Light"
                            onClick={() => setLightTheme()}
                        />
                        <FormControlLabel
                            value="dark"
                            control={<Radio />}
                            label="Dark"
                            onClick={() => setDarkTheme()}
                        />
                    </RadioGroup>
                </FormControl>
            </CardContent>
        </Card>
    );
};

export default Settings;
