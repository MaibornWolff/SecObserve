import {
    Card,
    CardContent,
    CardHeader,
    FormControl,
    FormControlLabel,
    Radio,
    RadioGroup,
    Stack,
    Typography,
} from "@mui/material";
import { Title, useTheme } from "react-admin";

import { getSettingListSize, getSettingTheme, saveSettingListSize, saveSettingTheme } from "./functions";

const UserSettings = () => {
    const [, setTheme] = useTheme();

    function setLightTheme() {
        setTheme("light");
        localStorage.setItem("theme", "light");
        saveSettingTheme("light");
    }

    function setDarkTheme() {
        setTheme("dark");
        localStorage.setItem("theme", "dark");
        saveSettingTheme("dark");
    }

    return (
        <Card sx={{ marginTop: 2 }}>
            <Title title="Settings" />
            <CardHeader title="Settings" />
            <CardContent>
                <Stack sx={{ width: "100%" }}>
                    <Typography variant="subtitle1">Theme</Typography>
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

                    <Typography variant="subtitle1" sx={{ marginTop: 2 }}>
                        List size
                    </Typography>
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

export default UserSettings;
