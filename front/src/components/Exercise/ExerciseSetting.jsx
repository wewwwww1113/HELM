import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useHistory } from "react-router-dom";
import { Container, Row, Col } from "react-bootstrap";
import Radium, { StyleRoot } from "radium";
import {
  TotalStyle,
  StartButton,
  modalStyle,
  modalTitle,
  fontNormal,
  fontBold,
  mainButton,
  modalBody,
  ExerciseInput,
  ExerciseSelect,
} from "./ExerciseSetting.style";
import {
  setExerciseType,
  setExerciseSet,
  setExerciseTime,
} from "../../store/modules/exerciseHistory";
import CloseIcon from "@mui/icons-material/Close";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Modal from "@mui/material/Modal";
import Button from "../Main/Button";
import Typography from "../Main/Typography";
import BannerLayout from "./BannerLayout";
import bannerImg from "../../assets/images/exerciseBanner.jpg";

export default function ExerciseSetting() {
  const dispatch = useDispatch();
  const history = useHistory();
  const ExerciseTypeList = [
    "사이드 레터럴 레이즈",
    "윗몸일으키기",
    "턱걸이",
    "팔굽혀펴기",
    "스쿼트",
    "런지",
  ];
  const { exercise } = useSelector((state) => state.exerciseHistory);
  const [breakTime, setBreakTime] = useState(0);

  const TypeSelect = ExerciseTypeList.map((type, index) => {
    return (
      <option key={index} data-index={index}>
        {type}
      </option>
    );
  });

  const exerciseSetting = (e) => {
    if (exercise.set === 0) {
      alert("목표 세트를 정해주세요.");
    } else if (exercise.time === 0) {
      alert("세트별 횟수를 정해주세요.");
    } else {
      history.push(`exercise/${breakTime}`);
    }
  };

  const typeChange = (e) => {
    dispatch(setExerciseType(e.target.selectedIndex + 1));
  };

  const setChange = (e) => {
    if (e.target.value < 1) {
      alert("세트 수가 너무 적습니다.");
      e.target.value = 0;
    } else {
      dispatch(setExerciseSet(e.target.value));
    }
  };

  const timeChange = (e) => {
    if (e.target.value < 1) {
      alert("세트별 횟수가 너무 적습니다.");
      e.target.value = 0;
    } else {
      dispatch(setExerciseTime(e.target.value));
    }
  };

  const breakTimeChange = (e) => {
    setBreakTime(e.target.value);
  };

  const [open, setOpen] = useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  return (
    <>
      <StyleRoot>
        <BannerLayout
          sxBackground={{
            backgroundImage: `url(${bannerImg})`,
            backgroundColor: "#7fc7d9",
            backgroundPosition: "center",
          }}
        >
          <img
            style={{
              display: "none",
            }}
            src={bannerImg}
            alt="increase priority"
          />
          <Typography
            color="inherit"
            align="center"
            variant="h2"
            marked="center"
            style={fontBold}
          >
            BUILD HEALTHY BODY
          </Typography>
          <Typography
            color="inherit"
            align="center"
            variant="h3"
            style={fontNormal}
            sx={{
              mb: 4,
              mt: {
                sx: 4,
                sm: 10,
              },
            }}
          >
            운동 전 5~10분간 준비운동은
            <br />
            부상을 예방하고 운동효과를 높여줍니다.
          </Typography>
          <Button
            variant="contained"
            size="large"
            component="a"
            style={mainButton}
            sx={{
              minWidth: 200,
            }}
            onClick={handleOpen}
          >
            시작버튼
          </Button>
        </BannerLayout>
        <Modal
          open={open}
          onClose={handleClose}
          aria-labelledby="modal-modal-title"
          aria-describedby="modal-modal-description"
        >
          <Box sx={modalStyle}>
            <Box sx={{ flexGrow: 1 }}>
              <Grid container spacing={2}>
                <Grid item xs={3}>
                  <div></div>
                </Grid>
                <Grid item xs={6}>
                  <div style={modalTitle}>MY운동 세팅</div>
                </Grid>
                <Grid item xs={3} sx={{ textAlign: "right" }}>
                  <CloseIcon
                    style={{ 
                      width: "30%", 
                      height: "100%", 
                      cursor: "pointer", 
                      '@media (max-width: 480px)': {
                        margin: '30px',
                        width: "50%", 
                      }, 
                    }}
                    onClick={handleClose}
                  />
                </Grid>
              </Grid>
            </Box>
            <Grid container spacing={1} style={modalBody}>
              <Grid item xs={12} sm={6}>
                운동
              </Grid>
              <Grid item xs={12} sm={6}>
                <ExerciseSelect onChange={typeChange}>
                  {TypeSelect}
                </ExerciseSelect>
              </Grid>
              <Grid item xs={12} sm={6}>
                목표 세트
              </Grid>
              <Grid item xs={12} sm={6}>
                <ExerciseInput
                  type="number"
                  placeholder="0"
                  onChange={setChange}
                ></ExerciseInput>
              </Grid>
              <Grid item xs={12} sm={6}>
                세트별 횟수
              </Grid>
              <Grid item xs={12} sm={6}>
                <ExerciseInput
                  type="number"
                  placeholder="0"
                  onChange={timeChange}
                ></ExerciseInput>
              </Grid>
              <Grid item xs={12} sm={6}>
                휴식 시간(초)
              </Grid>
              <Grid item xs={12} sm={6}>
                <ExerciseInput
                  type="number"
                  placeholder="0"
                  onChange={breakTimeChange}
                ></ExerciseInput>
              </Grid>
            </Grid>
            <div style={{ textAlign: "center" }}>
              <StartButton onClick={exerciseSetting}>시작</StartButton>
            </div>
          </Box>
        </Modal>
      </StyleRoot>
    </>
  );
}
