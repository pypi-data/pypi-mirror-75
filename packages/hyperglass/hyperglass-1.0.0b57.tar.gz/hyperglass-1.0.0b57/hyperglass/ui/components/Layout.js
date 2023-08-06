import * as React from "react";
import { useRef } from "react";
import { Flex, useColorMode } from "@chakra-ui/core";
import Header from "~/components/Header";
import Footer from "~/components/Footer";
import Greeting from "~/components/Greeting";
import useConfig, { useHyperglassState } from "~/components/HyperglassProvider";
import Debugger from "~/components/Debugger";

const bg = { light: "white", dark: "black" };
const color = { light: "black", dark: "white" };

const Layout = ({ children }) => {
  const config = useConfig();
  const { colorMode } = useColorMode();
  const { greetingAck, setGreetingAck } = useHyperglassState();
  const containerRef = useRef(null);

  return (
    <>
      <Flex
        w="100%"
        ref={containerRef}
        minHeight="100vh"
        bg={bg[colorMode]}
        flexDirection="column"
        color={color[colorMode]}
      >
        <Flex px={2} flex="0 1 auto" flexDirection="column">
          <Header layoutRef={containerRef} />
        </Flex>
        <Flex
          px={2}
          py={0}
          w="100%"
          as="main"
          flex="1 1 auto"
          textAlign="center"
          alignItems="center"
          justifyContent="start"
          flexDirection="column"
        >
          {children}
        </Flex>
        <Footer />
        {config.developer_mode && <Debugger />}
      </Flex>
      {config.web.greeting.enable && !greetingAck && (
        <Greeting
          greetingConfig={config.web.greeting}
          content={config.content.greeting}
          onClickThrough={setGreetingAck}
        />
      )}
    </>
  );
};

export default Layout;
