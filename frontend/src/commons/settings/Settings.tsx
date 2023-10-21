// import Card from "@mui/material/Card";
import { Box, Card, CardContent, CardHeader, FormControl, FormControlLabel, Radio, RadioGroup } from "@mui/material";
import { Title, useTheme } from "react-admin";

import { darkTheme, lightTheme } from "../layout/themes";
import { getSettingTheme, saveSettingTheme } from "./functions";

const Settings = () => {
    const [, setTheme] = useTheme();

    function setLightTheme() {
        setTheme(lightTheme);
        saveSettingTheme("light");
    }

    function setDarkTheme() {
        setTheme(darkTheme);
        saveSettingTheme("dark");
    }

    return (
        <Card sx={{ marginTop: 2 }}>
            <Title title="Settings" />
            <CardHeader title="Settings" />
            <CardContent>
                <Box sx={{ width: "10em", display: "inline-block" }}>Theme</Box>
                <FormControl>
                    <RadioGroup defaultValue={getSettingTheme()} name="radio-buttons-group" row>
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
