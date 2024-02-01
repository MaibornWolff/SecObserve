import {
    Box,
    Card,
    CardContent,
    CardHeader,
    FormControl,
    FormControlLabel,
    Radio,
    RadioGroup,
    Stack,
} from "@mui/material";
import { useState } from "react";
import { Title, useTheme } from "react-admin";

import { darkTheme, lightTheme } from "../layout/themes";
import { getSettingListSize, getSettingTheme, saveSettingListSize, saveSettingTheme } from "./functions";

const Settings = () => {
    const [previousTheme, setPreviousTheme] = useState(getSettingTheme());
    const [, setTheme] = useTheme();

    function setLightTheme() {
        setTheme(lightTheme);
        saveSettingTheme("light");
        if (previousTheme != "light") {
            window.location.reload();
        }
        setPreviousTheme("light");
    }

    function setDarkTheme() {
        setTheme(darkTheme);
        saveSettingTheme("dark");
        if (previousTheme != "dark") {
            window.location.reload();
        }
        setPreviousTheme("dark");
    }

    return (
        <Card sx={{ marginTop: 2 }}>
            <Title title="Settings" />
            <CardHeader title="Settings" />
            <CardContent>
                <Stack spacing={2} sx={{ width: "100%" }}>
                    <Box sx={{ width: "10em", display: "inline-block" }}>Theme</Box>
                    <FormControl>
                        <RadioGroup defaultValue={getSettingTheme()} name="radio-buttons-group-theme" row>
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
                    <Box sx={{ width: "10em", display: "inline-block" }}>List size</Box>
                    <FormControl>
                        <RadioGroup defaultValue={getSettingListSize()} name="radio-buttons-group-list-size" row>
                            <FormControlLabel
                                value="small"
                                control={<Radio />}
                                label="Small"
                                onClick={() => saveSettingListSize("small")}
                            />
                            <FormControlLabel
                                value="medium"
                                control={<Radio />}
                                label="Medium"
                                onClick={() => saveSettingListSize("medium")}
                            />
                        </RadioGroup>
                    </FormControl>
                </Stack>
            </CardContent>
        </Card>
    );
};

export default Settings;
