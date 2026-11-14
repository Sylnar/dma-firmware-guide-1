`timescale 1ns/1ps
module tb_guide_bar;
    logic clk = 0;
    always #5 clk = ~clk;
    logic rst = 1;
    logic [31:0] wr_addr = 0, wr_data = 0;
    logic [3:0] wr_be = 0;
    logic wr_valid = 0;
    logic [87:0] rd_req_ctx = 0;
    logic [31:0] rd_req_addr = 0;
    logic rd_req_valid = 0;
    wire [87:0] rd_rsp_ctx;
    wire [31:0] rd_rsp_data;
    wire rd_rsp_valid;
    integer checks = 0;
    guide_bar dut(.*);

    task automatic check(input bit ok, input string label_text);
        if (!ok) $fatal(1, "FAIL: %s", label_text);
        checks = checks + 1;
    endtask

    task automatic write_reg(input logic [31:0] addr,
                             input logic [31:0] data,
                             input logic [3:0] be);
        @(negedge clk);
        wr_addr = addr; wr_data = data; wr_be = be; wr_valid = 1;
        @(negedge clk);
        wr_valid = 0;
    endtask

    task automatic read_reg(input logic [31:0] addr,
                            input logic [31:0] expected,
                            input logic [87:0] context_value);
        @(negedge clk);
        rd_req_addr = addr; rd_req_ctx = context_value; rd_req_valid = 1;
        @(posedge clk); #1;
        check(!rd_rsp_valid, "no early response");
        @(negedge clk); rd_req_valid = 0;
        @(posedge clk); #1;
        check(rd_rsp_valid, "response valid");
        check(rd_rsp_data === expected, "response data");
        check(rd_rsp_ctx === context_value, "context preserved");
        @(posedge clk); #1;
        check(!rd_rsp_valid, "no duplicate response");
    endtask

    initial begin
        repeat (3) @(negedge clk);
        rst = 0;
        read_reg(0, 32'h47554944, 88'h1234);
        read_reg(4, 32'h00020001, 88'h5678);
        read_reg(8, 0, 88'h9abc);
        write_reg(8, 32'h11223344, 4'b1111);
        read_reg(8, 32'h11223344, 88'h1111);
        write_reg(8, 32'haabbccdd, 4'b0101);
        read_reg(8, 32'h11bb33dd, 88'h2222);
        write_reg(8, 32'hffffffff, 4'b0000);
        read_reg(8, 32'h11bb33dd, 88'h3333);
        write_reg(0, 0, 4'b1111);
        read_reg(0, 32'h47554944, 88'h4444);
        read_reg(32'h014, 0, 88'h5555);

        // Consecutive requests must retain their own data and context.
        @(negedge clk);
        rd_req_valid = 1; rd_req_addr = 0; rd_req_ctx = 88'h10;
        @(negedge clk);
        rd_req_addr = 4; rd_req_ctx = 88'h20;
        @(posedge clk); #1;
        check(rd_rsp_valid && rd_rsp_ctx == 88'h10 &&
              rd_rsp_data == 32'h47554944, "back-to-back first");
        @(negedge clk); rd_req_valid = 0;
        @(posedge clk); #1;
        check(rd_rsp_valid && rd_rsp_ctx == 88'h20 &&
              rd_rsp_data == 32'h00020001, "back-to-back second");
        @(posedge clk); #1;
        check(!rd_rsp_valid, "back-to-back drained");

        // Same-cycle write/read returns the old scratch snapshot.
        @(negedge clk);
        wr_addr = 8; wr_data = 32'hdeadbeef; wr_be = 15; wr_valid = 1;
        rd_req_addr = 8; rd_req_ctx = 88'h30; rd_req_valid = 1;
        @(negedge clk); wr_valid = 0; rd_req_valid = 0;
        @(posedge clk); #1;
        check(rd_rsp_valid && rd_rsp_data == 32'h11bb33dd,
              "read-during-write returns old data");
        @(posedge clk); #1;
        read_reg(8, 32'hdeadbeef, 88'h40);

        // Reset cancels an accepted request and clears writable state.
        @(negedge clk); rd_req_valid = 1; rd_req_addr = 0;
        @(negedge clk); rst = 1; rd_req_valid = 0;
        @(posedge clk); #1;
        check(!rd_rsp_valid, "reset cancels pending read");
        @(negedge clk); rst = 0;
        read_reg(8, 0, 88'h50);
        check(dut.cycles != 0, "cycle counter advances");
        $display("GUIDE_BAR_PASS checks=%0d", checks);
        $finish;
    end
    initial begin
        #20000;
        $fatal(1, "simulation timeout");
    end
endmodule
