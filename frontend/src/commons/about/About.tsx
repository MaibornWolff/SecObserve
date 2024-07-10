import InfoIcon from "@mui/icons-material/Info";
import {
    Button,
    Dialog,
    DialogContent,
    DialogTitle,
    Grid,
    Link,
    ListItemIcon,
    ListItemText,
    MenuItem,
    Stack,
    Typography,
} from "@mui/material";
import { Fragment, useState } from "react";

import { httpClient } from "../../commons/ra-data-django-rest-framework";

const About = () => {
    const get_version = "version_unkown";

    const [open, setOpen] = useState(false);
    const [backendVersion, setBackendVersion] = useState("...");

    const getBackendVersion = async () => {
        httpClient(window.__RUNTIME_CONFIG__.API_BASE_URL + "/status/version", {
            method: "GET",
        })
            .then((result) => {
                setBackendVersion(result.json.version);
            })
            .catch((error) => {
                console.warn(error);
            });
    };

    const handleClose = (event: object, reason: string) => {
        if (reason && reason == "backdropClick") return;
        setOpen(false);
    };

    const handleOk = () => setOpen(false);

    const handleOpen = () => {
        setOpen(true);
    };

    const OKButton = () => (
        <Button
            sx={{
                mr: "1em",
                direction: "row",
                justifyContent: "center",
                alignItems: "center",
            }}
            variant="contained"
            onClick={handleOk}
            color="inherit"
        >
            OK
        </Button>
    );

    if (backendVersion == "...") {
        getBackendVersion();
    }

    return (
        <Fragment>
            <MenuItem
                onClick={() => {
                    handleOpen();
                }}
            >
                <ListItemIcon>
                    <InfoIcon />
                </ListItemIcon>
                <ListItemText>About</ListItemText>
            </MenuItem>
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>About</DialogTitle>
                <DialogContent>
                    <Typography sx={{ marginBottom: 4 }}>
                        SecObserve gathers results about potential security flaws from various vulnerability scanning
                        tools and makes them available for assessment and reporting.
                    </Typography>
                    <Grid container spacing={2}>
                        <Grid item xs={4}>
                            <Typography>Backend version:</Typography>
                        </Grid>
                        <Grid item xs={8}>
                            <Typography>{backendVersion}</Typography>
                        </Grid>
                        <Grid item xs={4}>
                            <Typography>Frontend version:</Typography>
                        </Grid>
                        <Grid item xs={8}>
                            <Typography>{get_version}</Typography>
                        </Grid>
                        <Grid item xs={4}>
                            <Typography>Copyright:</Typography>
                        </Grid>
                        <Grid item xs={8}>
                            <Link
                                href="https://www.maibornwolff.de"
                                target="_blank"
                                rel="noreferrer"
                                sx={{ textDecoration: "none" }}
                            >
                                MaibornWolff GmbH
                            </Link>
                        </Grid>
                        <Grid item xs={4}>
                            <Typography>License:</Typography>
                        </Grid>
                        <Grid item xs={8}>
                            <Link
                                href="https://github.com/MaibornWolff/SecObserve/blob/dev/LICENSE.txt"
                                target="_blank"
                                rel="noreferrer"
                                sx={{ textDecoration: "none" }}
                            >
                                BSD 3-Clause
                            </Link>
                        </Grid>
                        <Grid item xs={4}>
                            <Typography>Source code: </Typography>
                        </Grid>
                        <Grid item xs={8}>
                            <Link
                                href="https://github.com/MaibornWolff/SecObserve"
                                target="_blank"
                                rel="noreferrer"
                                sx={{ textDecoration: "none" }}
                            >
                                https://github.com/MaibornWolff/SecObserve
                            </Link>
                        </Grid>
                    </Grid>
                    <Stack direction="row" justifyContent="center" alignItems="center" marginTop={4} spacing={2}>
                        <OKButton />
                    </Stack>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default About;
