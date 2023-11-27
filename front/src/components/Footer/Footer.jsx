import * as React from 'react';
import Grid from '@mui/material/Grid';
import Link from '@mui/material/Link';
import Container from '@mui/material/Container';
import Typography from '../Main/Typography';
import logo from '../../assets/images/logo.png';
import {
    footerBackground,
    regualrFontColor,
    fontBold,
//    contributor,
//    contributors,
//    Copyright,
    LogoImage,
} from './Footer.style';

export default function Footer() {
    const handleLogo = () => {
        window.scrollTo(0,0);
    };
    return (
        <Typography
            component="footer"
            style={ footerBackground }
            sx={{
                display: 'flex',
            }}>
            <Container
                sx={{
                    my: 8,
                    display: 'flex'
                }}>
                <Grid container spacing={5}>
                
                    <Grid item xs={12} sm={3}>
                    {/* <Grid item xs={6} sm={4} md={3}> */}
                        <Grid
                            container
                            direction="column"
                            sx={{
                                height: 100,
                                width: 50
                            }}>
                            <LogoImage src={ logo } alt="system logo" onClick={ handleLogo } />
                        </Grid>
                    </Grid>
                    

                </Grid>
            </Container>
        </Typography>
    );
}
