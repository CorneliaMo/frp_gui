
// frp_guiDlg.h: 头文件
//

#pragma once


// CfrpguiDlg 对话框
class CfrpguiDlg : public CDialogEx
{
// 构造
public:
	CfrpguiDlg(CWnd* pParent = nullptr);	// 标准构造函数

// 对话框数据
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_FRP_GUI_DIALOG };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV 支持


// 实现
protected:
	HICON m_hIcon;

	// 生成的消息映射函数
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()
public:
	afx_msg void OnBnClickedMfcbutton1();
	afx_msg void OnBnClickedMfcbutton2();
	CMFCButton m_startButton;
	afx_msg void OnBnClickedStartbutton();
	afx_msg void OnBnClickedRestartbutton();
	afx_msg void OnBnClickedAddbutton();
	afx_msg void OnBnClickedEditbutton();
	afx_msg void OnBnClickedDeletebutton();
	CListCtrl m_list;
	CMFCButton m_restartButton;
	CStatic m_statusText;
};
